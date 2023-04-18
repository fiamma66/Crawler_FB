from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from logging import getLogger
import logging
import pathlib
import re
import time
import logging.config

logger = getLogger('root')
logger.setLevel(logging.INFO)


class FaceBookCrawler:
    """
    :argument: url
    Facebook Page url to be Crawled

    :argument: path
    Executable WebDriver to be located
    Default is './chromedriver/chromedriver'

    :argument: userid
    Login Into Facebook ID

    :argument: passwd
    Password to Login

    Class Build By Parsing Url in
    Using Class Method crawl to start crawl
    """

    # Default Value
    COMMENT_DEEP_COUNT = 4
    LOGON_TIME = 10
    WAIT_ACTIVE_TIME = 20
    TIMEOUT = 10
    SCROLL_PAUSE_TIME = 2
    POST_COUNTER = 0
    POST_ID_PATTERN = re.compile(r"https?://.*?/.*?/\d+/posts/(\d+)/\?.*",
                                 re.I)
    LOGON_SELECTOR = (
        'div[class="x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 '
        "x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf "
        "xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 "
        "x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r "
        "x2lwn1j xeuugli x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq "
        "x1ja2u2z x1t137rt x3nfvp2 x1q0g3np x87ps6o x1lku1pv "
        "x1a2a7pz xtvsq51 xhk9q7s x1otrzb0 x1i1ezom x1o6z2jb "
        "x1vqgdyp x6ikm8r x10wlt62 xexx8yu xn6708d x1120s5i "
        'x1ye3gou"]'
    )
    IMAGE_CLASS_SELECTOR = 'div[class="x6ikm8r x10wlt62 x10l6tqk"]'
    IMAGE_IMG_SELECTOR = (
        'img[class="x1ey2m1c xds687c x5yr21d x10l6tqk '
        'x17qophe x13vifvy xh8yej3"]'
    )
    SINGLE_IMAGE_IMG_SELECTOR = (
        'img[class="x1ey2m1c xds687c x5yr21d '
        'x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r"]'
    )
    LOAD_REPLY_MORE_SELECTOR = (
        'div[class="x1i10hfl xjbqb8w xjqpnuy xa49m3k '
        "xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 "
        "x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n "
        "x9f619 x1ypdohk xdl72j9 xe8uvvx xdj266r "
        "x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli "
        "xexx8yu x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 "
        "x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj "
        "x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np "
        "x87ps6o x1a2a7pz x6s0dn4 xi81zsa x1iyjqo2 "
        'xs83m0k xsyo7zv xt0b8zv"]'
    )
    LOAD_SEE_MORE_SELECTOR = (
        'div[class="x1i10hfl xjbqb8w x6umtig x1b1mbwd '
        "xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 "
        "xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r "
        "xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 "
        "x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u "
        'x1s688f"]'
    )
    POST_BLOCK_SELECTOR = 'div[class="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"]'
    POST_ID_LOCATE_SELECTOR = (
        'span[class="x4k7w5x x1h91t0o x1h9r5lt xv2umb2 '
        "x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k "
        "xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j "
        'x1jfb8zj"]'
    )
    POST_ID_SELECTOR = (
        'a[class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y '
        "xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r "
        "x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 "
        "xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g "
        'xt0b8zv xo1l8bm"]'
    )

    POST_BODY_SELECTOR_REFILL = (
        'div[class*="x1iorvi4 x1pi30zi"]'
    )
    TEXT_BODY_SELECTOR_REFILL = (
        'div[class="x1e56ztr"]'
    )

    POST_COMMENT_BLOCK_SELECTOR = (
        'div[class="x168nmei x13lgxp2 x30kzoy '
        'x9jhf4c x6ikm8r x10wlt62"] > div > div['
        'class="x1jx94hy x12nagc"]'
    )
    POST_COMMENT_LIST_SELECTOR_L_MODE = (
        'div[class="x1i10hfl x1qjc9v5 '
        "xjqpnuy xa49m3k xqeqjp1 x2hbi6w "
        "x1ypdohk xdl72j9 x2lah0s xe8uvvx "
        "x2lwn1j xeuugli x1hl2dhg xggy1nq "
        "x1t137rt x1o1ewxj x3x9cwd x1e5q0jg "
        "x13rtm0m x3nfvp2 x1q0g3np x87ps6o "
        "x1a2a7pz xjyslct xjbqb8w x13fuv20 "
        "xu3j5b3 x1q0q8m5 x26u7qi x972fbf "
        "xcfux6l x1qhh985 xm0m39n x9f619 "
        "x1heor9g xdj266r x11i5rnm xat24cr "
        "x1mh8g0r xexx8yu x4uap5 x18d9i69 "
        "xkhd6sd x1n2onr6 x16tdsg8 x1ja2u2z "
        'xt0b8zv"]'
    )
    POST_COMMENT_MORE_SELECTOR_LOGON_MODE = (
        'div[class="x168nmei x13lgxp2 x30kzoy x9jhf4c x6ikm8r x10wlt62"]'
    )
    POST_COMMENT_BLOCK_SELECTOR_LOGON_MODE = (
        'div[class="x168nmei x13lgxp2 '
        "x30kzoy x9jhf4c x6ikm8r "
        'x10wlt62"] > div > div[class=" '
        'xzueoph"]'
    )
    POST_COMMENT_FLOAT_WINDOWS_L_MODE = (
        'div[class="xwya9rg x11i5rnm ' 'x1e56ztr x1mh8g0r xh8yej3"]'
    )

    POST_AUTHOR_AREA_SELECTOR = (
        'div[class="xu06os2 x1ok221b"]'
    )
    POST_AUTHOR_TEXT_SELECTOR = "strong > span"

    TEXT_BODY_SELECTOR = (
        'div[class="xu06os2 x1ok221b"]'
    )

    COMMENT_TEXT_SELECTOR = (
        'div[class="x1lliihq xjkvuk6 x1iorvi4"]'
    )

    def __init__(
            self,
            url,
            userid=None,
            passwd=None,
            path="./chromedriver/chromedriver",
            output_dir="./POST",
            log_config='./logging.conf',
    ):
        self.url = url
        self.userid = userid
        self.passwd = passwd
        self.exe = path
        self.output = pathlib.Path(output_dir)
        self.option = ChromeOptions()
        logging.config.fileConfig(log_config)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        if self.userid and self.passwd:
            self.logon_mode = True
        else:
            self.logon_mode = False

        # Testing Option
        self.option.add_argument("--lang=en-us")
        # Full Screen
        self.option.add_argument("window-size=1920,1080")
        self.option.add_experimental_option("detach", True)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        self.option.add_experimental_option("prefs", prefs)
        # Do Not Load Image
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # self.option.add_experimental_option('prefs', prefs)

        if self.exe:
            self.driver = webdriver.Chrome(
                executable_path=self.exe, chrome_options=self.option
            )
        else:
            self.driver = webdriver.Chrome(chrome_options=self.option)

    def open_and_wait(self):
        self.driver.get(self.url)

        try:
            post_element = EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.POST_BLOCK_SELECTOR)
            )
            WebDriverWait(self.driver, timeout=self.TIMEOUT) \
                .until(post_element)

        except TimeoutException:
            self.logger.error("Over Time ! Check Network Condition")

    def login(self):
        if not self.logon_mode:
            return
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="email"]') \
            .send_keys(self.userid)
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="pass"]'). \
            send_keys(self.passwd)
        self.driver.find_element(By.CSS_SELECTOR, self.LOGON_SELECTOR).click()
        try:
            post_element = EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.POST_BLOCK_SELECTOR)
            )
            WebDriverWait(self.driver, timeout=self.LOGON_TIME) \
                .until(post_element)
        except TimeoutException:
            self.logger.error("Over Time ! Check Network Condition")

    def output_post(self, postid, author, content, img_list, comment_list):
        """
        Writing Output To File , File Name Should be POST - ID
        :param postid: Post ID get From every post
        :param author: Author of Post
        :param content: Content of Post
        :param img_list: Image List of Post , Type: List
        :param comment_list: Comment List of Post , Type: List
        :return: If Output File Already Exists, Skipping Writing
        """
        if not self.output.exists():
            self.output.mkdir()

        outfile = self.output / postid
        if outfile.exists():
            return
        with open(outfile, "w", encoding="UTF8") as f:
            f.write(f"POSTID={postid}\n")
            f.write(f"AUTHOR={author}\n")
            f.write(f"CONTENT={content}\n")
            f.write(f"IMGLIST={img_list}\n")
            f.write(f"COMMENTLIST={comment_list}\n")

    def grab_image(self, element):
        """
        :param element: Text Body Element
        :return: List of Every Post Image
        """
        images_list = element.find_elements(
            By.CSS_SELECTOR, self.IMAGE_CLASS_SELECTOR
        )
        image_pocket = []
        for i in images_list:
            my_img = i.find_elements(By.CSS_SELECTOR, self.IMAGE_IMG_SELECTOR)
            if len(my_img) > 0:
                image_pocket.append(
                    my_img[0].get_attribute("src")
                )

        # Check Single Image
        images_list = element.find_elements(
            By.CSS_SELECTOR, self.SINGLE_IMAGE_IMG_SELECTOR
        )
        for i in images_list:
            image_pocket.append(i.get_attribute("src"))

        return image_pocket

    def _click(self, button_element, no_wait=False):
        """

        :param button_element: Button Element Interactable
        :return: Perform Click Action
        """
        try:
            ActionChains(self.driver).click(button_element).perform()
            if no_wait:
                time.sleep(self.SCROLL_PAUSE_TIME)
        except ElementNotInteractableException:
            pass

    def click_load_comment(self, element):
        """

        :param element: Post Block Element
        :return: Click See Previous Comment and return
        1. Button to Release (Logon Mode Only)
        2. Comment Body Element
        """
        if not self.logon_mode:
            if (
                    len(
                        element.find_elements(
                            By.CSS_SELECTOR, self.POST_COMMENT_BLOCK_SELECTOR
                        )
                    )
                    > 0
            ):
                comment_area = element.find_element(
                    By.CSS_SELECTOR, self.POST_COMMENT_BLOCK_SELECTOR
                )
            else:
                self.logger.warning("No Comment Area")
                return None, None

            for i in range(self.COMMENT_DEEP_COUNT):
                for button in comment_area.find_elements(
                        By.CSS_SELECTOR, self.LOAD_REPLY_MORE_SELECTOR
                ):
                    if "隱藏" in button.text or "Hide" in button.text:
                        continue

                    self._click(button, no_wait=True)
                time.sleep(self.SCROLL_PAUSE_TIME)
            return None, comment_area
        else:
            # Logon Mode
            if (
                    len(
                        element.find_elements(
                            By.CSS_SELECTOR,
                            self.POST_COMMENT_LIST_SELECTOR_L_MODE
                        )
                    )
                    > 0
            ):
                float_button = element.find_elements(
                    By.CSS_SELECTOR, self.POST_COMMENT_LIST_SELECTOR_L_MODE
                )[0]
                # First Click To Load Comment
                self._click(float_button)
                _float_windows = EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.POST_COMMENT_FLOAT_WINDOWS_L_MODE)
                )
                try:
                    WebDriverWait(self.driver, timeout=self.LOGON_TIME).until(
                        _float_windows
                    )
                except TimeoutException:
                    self._click(float_button)
                # Float Window will out of comment block
                # Re-locate
                float_windows = self.driver.find_elements(
                    By.CSS_SELECTOR, self.POST_COMMENT_FLOAT_WINDOWS_L_MODE
                )
                if len(float_windows) > 0:
                    float_window = float_windows[0]
                    for i in range(self.COMMENT_DEEP_COUNT):
                        for button in float_window.find_elements(
                                By.CSS_SELECTOR, self.LOAD_REPLY_MORE_SELECTOR
                        ):
                            if "隱藏" in button.text or "Hide" in button.text:
                                continue
                            self._click(button, no_wait=True)
                        time.sleep(self.SCROLL_PAUSE_TIME)
                    return float_button, float_window
                else:
                    # Low Comment, Can't Use Float Windows
                    self.logger.warning("Float Windows Not Appear !")
                    if (
                            len(
                                element.find_elements(
                                    By.CSS_SELECTOR,
                                    self.POST_COMMENT_BLOCK_SELECTOR
                                )
                            )
                            > 0
                    ):
                        comment_area = element.find_element(
                            By.CSS_SELECTOR, self.POST_COMMENT_BLOCK_SELECTOR
                        )
                    else:
                        self.logger.warning("No Comment Area")
                        return None, None

                    for i in range(self.COMMENT_DEEP_COUNT):
                        for button in comment_area.find_elements(
                                By.CSS_SELECTOR, self.LOAD_REPLY_MORE_SELECTOR
                        ):
                            if "隱藏" in button.text or "Hide" in button.text:
                                continue

                            self._click(button, no_wait=True)
                        time.sleep(self.SCROLL_PAUSE_TIME)
                    return None, comment_area
            else:
                self.logger.debug("No Comment To Grab")
                return None, None

    def click_see_more(self, element):
        """

        :param element: Post Block or Comment Block
        :return: Click See More Action
        """
        self.logger.debug(element.get_attribute("innerHTML"))
        try:
            button = element.find_element(
                By.CSS_SELECTOR, self.LOAD_SEE_MORE_SELECTOR
            )
            self._click(button)
        except NoSuchElementException:
            self.logger.debug("No See More")
            pass

    def grab_comment(self, element):
        """

        :param element: Post Block Element
        :return: Every Comment Pocket List
        """

        button, comment_area = self.click_load_comment(element)

        comment_pocket = []
        self.logger.debug("Grabing every Comment")
        if not comment_area:
            return comment_pocket
        comment_li = comment_area.find_elements(
            By.CSS_SELECTOR, self.COMMENT_TEXT_SELECTOR
        )
        for comment in comment_li:
            comment_pocket.append(comment.text)
            # print("Appending Comment %s" % li.text)

        if self.logon_mode and button:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(self.SCROLL_PAUSE_TIME)

        return comment_pocket

    def grab_post(self):
        for i, every_post in enumerate(
                self.driver.find_elements(By.CSS_SELECTOR,
                                          self.POST_BLOCK_SELECTOR)
        ):
            if self.POST_COUNTER > i:
                continue
            else:
                self.POST_COUNTER += 1

            self.logger.info(f"===========  POST {i}  ================")

            ActionChains(self.driver).scroll_to_element(every_post).perform()
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Check Post ID
            post_id_elemnts = every_post.find_elements(
                By.CSS_SELECTOR, self.POST_ID_SELECTOR
            )
            if (
                    len(post_id_elemnts)
                    > 0
            ):
                try:
                    ec = EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, self.POST_ID_LOCATE_SELECTOR)
                    )
                    WebDriverWait(self.driver, timeout=self.WAIT_ACTIVE_TIME). \
                        until(ec)
                    ActionChains(self.driver).move_to_element(
                        every_post.find_elements(
                            By.CSS_SELECTOR, self.POST_ID_LOCATE_SELECTOR
                        )[0]
                    ).perform()
                except TimeoutException:
                    self.logger.error("Moving To get Post ID fail")
                    pass
                rw_postid = every_post.find_elements(
                    By.CSS_SELECTOR, self.POST_ID_SELECTOR
                )[0].get_attribute("href")
                if re.match(self.POST_ID_PATTERN, rw_postid):
                    postid = re.match(self.POST_ID_PATTERN, rw_postid).group(1)
                else:
                    self.logger.warning(
                        f"No PostID Found ! Row postID is {rw_postid}"
                    )
                    postid = "{} - {}".format(i, time.time())
            else:
                self.logger.error(f"Cant Select postID, Check POST {i}")
                postid = "{} - {}".format(i, time.time())

            if (
                    self.logon_mode
                    and len(
                    every_post.find_elements(
                        By.CSS_SELECTOR, self.TEXT_BODY_SELECTOR
                        )
                    )
                    > 0
            ):
                text_body = every_post.find_elements(
                    By.CSS_SELECTOR, self.TEXT_BODY_SELECTOR
                )[2]

                if not str.strip(text_body.text):
                    self.logger.warning("Refill Post Body")
                    text_body_first = every_post.find_element(
                        By.CSS_SELECTOR, self.POST_BODY_SELECTOR_REFILL
                    )
                    text_body_child = text_body_first.find_element(
                        By.CSS_SELECTOR, self.TEXT_BODY_SELECTOR_REFILL
                    )
                    # Find Parent Element
                    text_body = text_body_child.find_element(
                        By.XPATH, '..'
                    )
                    self.logger.debug(text_body.get_attribute("innerHTML"))
                    self.click_see_more(text_body)
                else:
                    self.click_see_more(text_body)

            else:
                text_body = None

            self.logger.debug(f"POST ID is {postid}")

            _author = every_post.find_element(
                By.CSS_SELECTOR, self.POST_AUTHOR_AREA_SELECTOR
            )
            author = _author.find_element(
                By.CSS_SELECTOR, self.POST_AUTHOR_TEXT_SELECTOR
            ).text
            self.logger.debug(f"Author is {author}")
            if text_body:
                content = text_body.text
                self.logger.debug(f"Body text {text_body.text}")
            else:
                self.logger.warning('No Body Content')
                content = None

            image_pocket = self.grab_image(every_post)
            self.logger.debug(f"Image List : {image_pocket}")

            # Comment Area
            comment_pocket = self.grab_comment(every_post)
            self.logger.debug(f"Comment List : {comment_pocket}")

            self.logger.debug("Writing To Output")
            self.output_post(
                postid=postid,
                author=author,
                content=content,
                img_list=image_pocket,
                comment_list=comment_pocket,
            )

    def scroll_down(self):
        """

        :return: (INT) Page Height
        """
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(self.SCROLL_PAUSE_TIME)

        return self.driver.execute_script("return document.body.scrollHeight")

    def start(self):
        self.open_and_wait()
        self.login()
        time.sleep(self.LOGON_TIME)
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )
        self.logger.debug(f"Recording Page Height : {last_height}")
        for i in range(3):
            # First Scroll
            self.scroll_down()

        while True:
            new_hieht = self.scroll_down()
            if new_hieht == last_height:
                break

            self.grab_post()
