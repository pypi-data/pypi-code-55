from wordpress import WordPress

url = "http://www.technologyinfos.com/courses"
login_url = "http://www.technologyinfos.com/courses/wp-admin"
usr = "kurt3n1z"
pwd = "WeWY!3%7`A/[9"

wp = WordPress(url, login_url, 'chromedriver', user_agent=True)
wp.wp_login(usr, pwd)
wp.maximize_window()
# wp.post_new("add", "z", "wp", "angular-programming", "Excerpt........")
# wp.post_new("add", "y", "yp", "angular-programming", "Excerpt........")
docx = 'C:\\Users\\AX\\Downloads\\doc\\Best-Free-Keyword-Research-Tools.docx'
# docx = 'E:\\WorkStation\\Blogs\\techcrench.com\\articles\\Best Gaming Keyboards for 2019 - Copy.docx'
# wp.post_new("add", "y", "yp", "angular-programming", "Excerpt........", docx)

# html = 'E:\\WorkStation\\Blogs\\techcrench.com\\articles\\Best Gaming Keyboards for 2019 - Copy.html'
# wp.post_content_block_html(html)

wp.post_new("add")
html = 'E:\\WorkStation\\Blogs\\techcrench.com\\articles\\Best Gaming Keyboards for 2019 - Copyf.html'
wp.post_content_from_file(html)

# wp.post_from_pdf('file:///F:/University/8B/Bio/assignment/Groups%20for%20Assignments.pdf')
# wp.post_new("add")
# wp.post_discussion(False, False)
# wp.post_status('public', None, True, True)
# wp.post_status('private')
# wp.post_status('password', 'ffffff')
# wp.post_content_block_heading("Head")
# wp.post_content_block_heading("Head", 'default', '#1bbafe')
wp.post_content_block_heading("Head", 'h1', 'center', '#1bbafe')
# wp.post_content_block_heading("Head", 'h1', '#1bbafe')
# wp.post_content_block_heading("Head", 'h2', '#1bbafe')
# wp.post_content_block_heading("Head", 'h3', '#1bbafe')
# wp.post_content_block_heading("Head", 'h4', '#1bbafe')
# wp.post_content_block_heading("Head", 'h5', '#1bbafe')
# wp.post_content_block_heading("Head", 'h6', '#1bbafe')
paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et " \
            "dolore magna aliqua. Diam maecenas sed enim ut. Suspendisse interdum consectetur libero id faucibus " \
            "nisl tincidunt eget. Sagittis orci a scelerisque purus semper eget duis at tellus. Vitae ultricies leo " \
            "integer malesuada nunc. Pharetra magna ac placerat vestibulum lectus mauris ultrices eros. Auctor augue " \
            "mauris augue neque gravida in fermentum et. Orci ac auctor augue mauris augue neque gravida in " \
            "fermentum. Maecenas accumsan lacus vel facilisis volutpat. Enim neque volutpat ac tincidunt vitae " \
            "semper quis lectus nulla. Sed turpis tincidunt id aliquet risus feugiat. Quis risus sed vulputate odio " \
            "ut enim blandit volutpat."
# paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et "
# wp.post_content_block_paragraph(paragraph, 'large', None, True, '#1bbafe', '#00a337')
# wp.post_content_block_paragraph(paragraph, None, 32, True, '#1bbafe', '#00a337')
## wp.post_content_block_paragraph(paragraph, 'right', None, 32, True, '#1bbafe', '#00a337')
# wp.post_content_block_html(docx)
# wp.post_save_draft()
# wp.post_format('gallery')
img_name = "angular-programming"
# wp.post_content_block_image(img_name)
# wp.post_content_block_image(img_name, None, None, True, "angular", "full", 100)
img_url = "https://yt3.ggpht.com/a/AATXAJwwH1OmjkYlBGpmwgaSgU4WVRPD3jvwk1aVxw=s500-c-k-c0xffffffff-no-rj-mo"
alt = "netD"
# wp.post_content_block_image(None, alt, img_url, 'left', True, alt, "thumbnail", 400, 400, 50)
# wp.post_content_block_paragraph(paragraph, 'large', None, True, '#1bbafe', '#00a337')
wp.post_content_block_image(None, alt, img_url, 'center', True, alt, "full", 400, 400, 100)
# wp.post_content_block_paragraph(paragraph, None, 32, True, '#1bbafe', '#00a337')
# wp.post_content_block_image(None, alt, img_url, 'right', True, alt, "thumbnail", 400, 400, 75)
# wp.post_content_block_list(paragraph)
# wp.post_content_block_list(paragraph, True)
# wp.post_content_block_list(paragraph, True, 11)
# wp.post_content_block_list(paragraph, True, None, True)
# wp.post_content_block_list(paragraph, True, 55, True)
wp.post_publish()
wp.post_switch_to_draft()
# wp.post_publish()
# wp.post_url('asdasa-wqeqwsss-sdad')
# wp.post_update()

print(wp.get_errors)
print("")
print(wp.get_completed)

input('Press Enter')
wp.close()
