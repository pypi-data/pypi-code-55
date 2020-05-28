import xadmin
from xadmin.filters import RelatedFieldListFilter, manager
from xadmin.layout import Fieldset, Row, Container

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin.models import LogEntry


from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin

from xadmin import views


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting:
    enable_themes = True  # 开启主题功能
    use_bootswatch = True  # 多种主题可选


@xadmin.sites.register(views.CommAdminView)
class GlobalSettings:
    """
    后台修改
    """
    site_title = '后台管理'
    site_footer = '北京中水科工程总公司'

    # global_search_models = [Post, ]

    global_models_icon = {
        Category: "fa fa-laptop",
        Post: "fa fa-circle",
        Tag: "fa fa-cloud",

    }
    menu_style = 'default'  # 'accordion'开启分组折叠


class PostInline:
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1  # 控制额外多几个
    model = Post



@xadmin.sites.register(Category)
class CategoryAdmin(object):
    list_display = ('name', 'status', 'is_nav', 'created_time',  'post_count')
    fields = ('name', 'status', 'is_nav', 'owner')
    # inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(object):
    list_display = ('name', 'status', 'created_time', 'post_count')
    fields = ('name', 'status', )

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # 展示页面
    form = PostAdminForm
    list_display = [
        'title',  'category',  'status', 'owner', 'created_time', 'operator'
    ]
    list_display_links = ['title']
    # list_filter = [CategoryOwnerFilter, OwnerFilter]
    list_filter = ['category']
    search_fields = ['title', 'category__name']
    filter_horizontal = ('tag',)
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    # save_on_top = True
    exclude = ('owner',)
    # fields = ('category', 'title',  'desc',  'status',  'content', 'tag', )
    form_layout = (
        Fieldset(
            "基础配置",
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            "内容信息",
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        ),

    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
            # self.model_admin_url('change', obj.id)

        )
    operator.short_description = '操作'




