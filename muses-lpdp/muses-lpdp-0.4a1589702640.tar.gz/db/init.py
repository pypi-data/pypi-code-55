from random import randint


def init(sender, **kwargs):
    import lorem
    from django.conf import settings
    import logging
    from datetime import date
    logger = logging.getLogger(__name__)
    import os
    from django.db import IntegrityError
    from ruamel.yaml import YAML
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    from db.models import SiteParam, Section, Tag, Faq, License, Post
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    VARS_PATH = os.getenv("VARS_PATH", BASE_DIR + "/vars_path")

    with open(f"{VARS_PATH}{os.path.sep}secrets.yml", "r") as secrets_file:
        secrets_content = secrets_file.read()
        yaml = YAML(typ="safe")
        SECRETS_SAFE = yaml.load(secrets_content)

        member = get_user_model()

        try:
            member.objects.create_superuser(
                username=SECRETS_SAFE['superuser_username'],
                email=SECRETS_SAFE['superuser_email'],
                date_of_birth=date.fromtimestamp(0),
                password=SECRETS_SAFE['superuser_password'])
        except IntegrityError:
            pass

        administrators_group = settings.MUSES.get("ADMINISTRATORS_GROUP", "muses_administrators")
        moderators_group = settings.MUSES.get("MODERATORS_GROUP", "muses_moderators")
        correctors_group = settings.MUSES.get("CORRECTORS_GROUP", "muses_correctors")

        Group.objects.bulk_create([
            Group(name=administrators_group),
            Group(name=moderators_group),
            Group(name=correctors_group),
        ], ignore_conflicts=True)

        super_user = member.objects.get(username=SECRETS_SAFE['superuser_username'])

        super_user.groups.add(Group.objects.get(name=administrators_group).id)
        super_user.groups.add(Group.objects.get(name=moderators_group).id)
        super_user.groups.add(Group.objects.get(name=correctors_group).id)

        # Add site params
        SiteParam.objects.bulk_create([
            SiteParam(key="site_title", value="Muses"),
            SiteParam(key="site_facebook_url",
                      value="https://www.facebook.com/pages/La-Passion-des-Po%C3%A8mes/107892505902908"),
            SiteParam(key="site_twitter_url", value="https://twitter.com/passionpoemes"),
        ], ignore_conflicts=True)

        # Add sections
        Section.objects.bulk_create([
            Section(short_name="texts", name="Les Ecrits", order=0),
            Section(short_name="events", name="Les Evénementiels", order=1),
            Section(short_name="literarygames", name="Les Jeux Littéraires", order=2),
            Section(short_name="discussions", name="Discussions", order=3),
            Section(short_name="news", name="Actualités", order=4),
            Section(short_name="management", name="Gestion", order=5),
        ], ignore_conflicts=True)

        section_mgmt = Section.objects.get(short_name="management")

        section_mgmt.groups.add(Group.objects.get(name=administrators_group).id)
        section_mgmt.groups.add(Group.objects.get(name=moderators_group).id)

        # Add tags
        Tag.objects.bulk_create([
            Tag(name="Acrostiches", type=Tag.CATEGORY, mature=False),
            Tag(name="Autres poèmes", type=Tag.CATEGORY, mature=False),
            Tag(name="Ballade", type=Tag.FORM, mature=False),
            Tag(name="Chanson", type=Tag.FORM, mature=False),
            Tag(name="Contes d'horreur", type=Tag.CATEGORY, mature=True),
            Tag(name="Contes fantastiques", type=Tag.CATEGORY, mature=False),
            Tag(name="Contrerime", type=Tag.FORM, mature=False),
            Tag(name="De tout et de rien", type=Tag.CATEGORY, mature=False),
            Tag(name="Ghazel", type=Tag.FORM, mature=False),
            Tag(name="Haï-kaï", type=Tag.FORM, mature=False),
            Tag(name="Holorime", type=Tag.FORM, mature=False),
            Tag(name="Lai", type=Tag.FORM, mature=False),
            Tag(name="Lettres ouvertes", type=Tag.CATEGORY, mature=False),
            Tag(name="Nouvelles littéraires", type=Tag.CATEGORY, mature=False),
            Tag(name="Ode", type=Tag.FORM, mature=False),
            Tag(name="Pantorime", type=Tag.FORM, mature=False),
            Tag(name="Pantoum", type=Tag.FORM, mature=False),
            Tag(name="Poème en prose", type=Tag.FORM, mature=False),
            Tag(name="Poèmes collectifs", type=Tag.CATEGORY, mature=False),
            Tag(name="Poèmes d'amitié", type=Tag.CATEGORY, mature=False),
            Tag(name="Poèmes d'amour", type=Tag.CATEGORY, mature=False),
            Tag(name="Poèmes loufoques", type=Tag.CATEGORY, mature=False),
            Tag(name="Poèmes par thèmes", type=Tag.CATEGORY, mature=False),
            Tag(name="Poèmes tristes", type=Tag.CATEGORY, mature=False),
            Tag(name="Rondeau redoublé", type=Tag.FORM, mature=False),
            Tag(name="Rondeau", type=Tag.FORM, mature=False),
            Tag(name="Rondel", type=Tag.FORM, mature=False),
            Tag(name="Sonnet irrégulier", type=Tag.FORM, mature=False),
            Tag(name="Sonnet marotique", type=Tag.FORM, mature=False),
            Tag(name="Sonnet", type=Tag.FORM, mature=False),
            Tag(name="Tanka", type=Tag.FORM, mature=False),
            Tag(name="Terza rima", type=Tag.FORM, mature=False),
            Tag(name="Textes d'opinion", type=Tag.CATEGORY, mature=False),
            Tag(name="Textes d'opinion", type=Tag.CATEGORY, mature=False),
            Tag(name="Textes érotiques", type=Tag.CATEGORY, mature=True),
            Tag(name="Théâtre & Scénario", type=Tag.CATEGORY, mature=False),
            Tag(name="Triolet", type=Tag.FORM, mature=False),
            Tag(name="Villanelle", type=Tag.FORM, mature=False),
            Tag(name="Virelai", type=Tag.FORM, mature=False),
        ], ignore_conflicts=True)

        # add Faq
        for n in range(70):
            Faq.objects.bulk_create(
                [
                    Faq(order=n, question=f"question {str(n)}?", answer=f"response {str(n)}.")
                ], ignore_conflicts=True
            )

        # add License
        License.objects.bulk_create([
            License(
                name="Copyright standard",
                text="",
                active=True
            ),
            License(
                name="Creative Commons - Attribution (CC BY)",
                text="",
                active=True
            ),
            License(
                name="Creative Commons - Attribution ShareAlike (CC BY-SA)",
                text="",
                active=True
            ),
            License(
                name="Creative Commons - Attribution-NoDerivs (CC BY-ND)",
                text="",
                active=True
            ),
            License(
                name="Creative Commons - Attribution-NonCommercial (CC BY-NC)",
                text="",
                active=True
            ),
            License(
                name="Creative Commons - Attribution-NonCommercial-ShareAlike (CC BY-NC-SA)",
                text="",
                active=True
            ),
            License(
                name="Creative Commons - Attribution-NonCommercial-NoDerivs (CC BY-NC-ND)",
                text="",
                active=True
            ),

        ], ignore_conflicts=True)

        if member.objects.count() < 100:
            for n in range(100):
                try:
                    member.objects.create_user(
                        username=f"username {str(n)}",
                        email=f"mail{str(n)}@domain.mail",
                        date_of_birth=date.fromtimestamp(0),
                        password=f"@zerty1234",
                        first_name=f"firstname {str(n)}",
                        last_name=f"lastname {str(n)}",
                        web_site="https://google.com",
                        job="job",
                        postal_address=lorem.sentence(),
                        postal_address_2=lorem.sentence(),
                        postal_city="92XXX",
                        story=lorem.paragraph()
                    )
                    m = member.objects.filter(username__exact=f"username {str(n)}").first()
                    posts = Post.objects.filter(author_id__exact=m.id)
                    if posts.count() == 0:
                        nb_posts = randint(1, 5)
                        for i in range(nb_posts):
                            post = Post(
                                title=lorem.sentence(),
                                summary=lorem.paragraph(),
                                content=lorem.paragraph(),
                                status=Post.PUBLISHED,
                                author=m,
                                section=Section.objects.filter(short_name__exact="texts").first(),
                            )
                            post.save()
                except IntegrityError as e:
                    logger.warning(f"error on create member: {e.with_traceback()}")
