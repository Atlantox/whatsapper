from time import sleep
from playwright.async_api import async_playwright, Playwright, Locator

class Whatsapper:
    '''
    Send automatic messages via WhatsApp Web (https://web.whatsapp.com/). Compatible with chromium and firefox
    '''
    def __init__(self, debug=True):
        self.url = 'https://web.whatsapp.com/'
        self.profile_image_base_url = 'https://media-mia3-1.cdn.whatsapp.net/v/'
        self.lastContact = None
        self.debug = debug
        self.admittedBrowsers = ('chromium', 'firefox', 'edge',)

        #self.WhatsAppTextBox = 'p.selectable-text.copyable-text'
        #self.WhatsAppInsideTextBox = 'span.selectable-text.copyable-text'

    async def OpenWhatsAppWeb(self, playwright:Playwright, targetBrowser:str):
        '''
        Open the WhatsApp Web using the selected browser
        '''
        if targetBrowser not in self.admittedBrowsers:
            raise Exception('Invalid browser. Available browsers:', str(self.admittedBrowsers))
        
        myBrowser = playwright.chromium

        if targetBrowser == 'firefox':
            myBrowser = playwright.firefox

        if targetBrowser == 'edge':
            self.browser = await myBrowser.launch_persistent_context('./user-data', headless=False, channel='msedge')
        else:
            self.browser = await myBrowser.launch_persistent_context('./user-data', headless=False)

        self.page = await self.browser.new_page()
        self.PrintDebug('[INFO]: Opening WhatsApp Web...')
        await self.page.goto(self.url)

    async def WaitLogin(self):
        '''
        Wait indefinitely until the users finish the login process in WhatsApp Web
        '''
        loggedIn = False
        times = 0
        while not loggedIn:
            times += 1
            self.PrintDebug('[WAITING]: Waiting for user login')

            if times > 10:
                popUpsClicked = await self.TryClosePopUps()
                if popUpsClicked == 0:
                    print('[ADVICE]: Make sure you close all pop-up windows')

            sleep(2)

            images = await self.page.locator('img').all()
            if len(images) == 0:
                continue

            for img in images:
                src = await img.get_attribute('src')
                if self.profile_image_base_url in src:
                    loggedIn = True
                    break

        self.PrintDebug('[INFO]: User login detected')

    async def SendMessages(self, messages:list[tuple], targetBrowser='chromium'):
        '''
        Recieve a list of 2-element tuples. The first element is the contact name and the second the message to send
        '''
        async with async_playwright() as playwright:
            await self.OpenWhatsAppWeb(playwright, targetBrowser)
            await self.WaitLogin()

            for message in messages:                
                await self.HandleMessage(message[0], message[1])  

            self.PrintDebug('All messages processed. Closing browser...')
            sleep(6)
            await self.browser.close()

    async def HandleMessage(self, contactName:str, message:str):
        '''
        Click on the contact and write the message
        '''
        if self.lastContact != contactName:            
            targetContact = await self.GetContact(contactName)

            if targetContact is None:
                self.PrintDebug(f'[WARNING]: Contact "{contactName}" not found. Ignoring message "{message}"')
                return
            
            self.PrintDebug(f'[INFO]: Selecting contact {contactName}')
            self.lastContact = contactName
            await targetContact.click()
            sleep(1.5)

        self.PrintDebug(f'[INFO]: Writting message "{message}"')
        await self.page.keyboard.type(message)
        await self.page.keyboard.press('Enter')
        sleep(1.5)            
            
    async def GetContact(self, contactName:str)->None|Locator:
        '''
        Search the contact button and return it. If the contact aren't found, returns None
        '''
        sleep(2.5)

        contacts = await self.page.locator(f'[title="{contactName}"]').all()
        if len(contacts) == 0:
            targetContact = None
        
        for contact in contacts:
            dir = await contact.get_attribute('dir')
            title = await contact.get_attribute('title')
            if [dir, title] == ['auto', contactName]:
                targetContact = contact
        
        return targetContact
    
    async def TryClosePopUps(self):
        '''
        Try different methods to close pop ups automatically
        '''
        clicks = 0
        maybePopUps = ['Continuar', 'Continue', 'Entendido', 'Ok']

        for popup in maybePopUps:
            for li in await self.page.get_by_text(popup, exact=True).all():
                clicks += 1
                await li.click()

        await self.page.keyboard.press('Enter')
        await self.page.keyboard.press('Escape')
        return clicks

    
    def PrintDebug(self, message:str):
        '''
        Print a debug message explaning the current program execution. Only displays if Whatsapper.debug is True
        '''
        if self.debug:
            print(message)