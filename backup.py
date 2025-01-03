import datetime
import os
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:

    # Check the envvars have been setup correctly
    url = os.getenv('PP_URL', '')
    username = os.getenv('PP_USERNAME', '')
    password = os.getenv('PP_PASSWORD', '')
    dbname = os.getenv('PP_DATABASE', '')
    backupname = os.getenv('PP_BACKUPNAME', username)

    for envvar in ['PP_URL', 'PP_USERNAME', 'PP_PASSWORD', 'PP_DATABASE']:
        if (envvar not in os.environ) or (os.getenv(envvar) == ''):
            raise EnvironmentError("Failed because {} is not set to a value.".format(envvar))      

    # Start the playwright session
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)

    # Select the database
    page.locator("select[name=\"auth\\[server\\]\"]").select_option("mysql8")

    # Enter credentials
    page.locator("#username").fill(username)
    page.locator("input[name=\"auth\\[password\\]\"]").fill(password)
    page.locator("input[name=\"auth\\[db\\]\"]").fill(dbname)
    page.get_by_role("button", name="Login").click()

    # Select the export option
    page.get_by_role("link", name="Export").click()

    # Choose the export settings
    page.get_by_label("gzip").check()
    page.locator("select[name=\"db_style\"]").select_option("DROP+CREATE")

    # Save the download
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Export").click()
    download = download_info.value

    # Wait for the download process to complete and save the downloaded file somewhere
    backuptime = datetime.datetime.now()
    if backupname:
        download.save_as("/dl/{0}_{1}.sql.gz".format(backuptime.strftime("%Y%m%d-%H%M%S"), backupname))
    else:
        download.save_as("/dl/{0}_{1}".format(backuptime.strftime("%Y%m%d-%H%M%S"), download.suggested_filename))

    # Logout
    page.get_by_role("button", name="Logout").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

# EOF

