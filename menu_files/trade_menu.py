import pygame
from sprite_files.hud import Textbox, UiButton
from SETTINGS import *


class TradeMenu(pygame.sprite.Sprite):
    def __init__(self, group:pygame.sprite.Group, owner:pygame.sprite.Sprite) -> None:
        super().__init__(group)
        self.group:pygame.sprite.Group = group
        self.is_active:bool = False
        self.buy_cart:list = []
        self.sell_cart:list = []
        self.z:int = overlay_layers['menu']
        self.owner:pygame.sprite.Sprite = owner
        self._menu_setup()
        self.group.remove(element for element in self.menu_ui)  #remove from group to prevent from rendering.

    def _menu_setup(self) -> None:
        """set the position for each element of the menu and assign its logic"""
        #menu setup
        self.image = pygame.image.load('images/hud/shop_bar.png')
        self.rect = self.image.get_rect(centerx=screen_width/2, bottom=screen_height)

        #items to display setup
        self.buy_button:UiButton = UiButton(self.group, button_text='Buy', button_func=self._buy, refrence_rect=self.rect, topleft_offset=(403,22))
        self.sell_button:UiButton = UiButton(self.group, button_text='Sell', button_func=self._sell, refrence_rect=self.rect, topleft_offset=(39,22))
        self.gold_textbox:Textbox = Textbox(self.group, self, offset=(239, 55), position='relative')
        self.buttons:list[UiButton] = [self.buy_button, self.sell_button]
        self.temp_buttons:list[UiButton] = []
        self.menu_ui:list = [self, self.buy_button, self.sell_button, self.gold_textbox]

    def show_menu(self, interactor) -> None:
        self.interactor = interactor
        self.transactable_spaces = []
        self.transactable_spaces.extend(self.owner.inventory_ui.setup_trading())
        self.transactable_spaces.extend(self.interactor.inventory_ui.setup_trading())
 
        self._setup_trade_buttons('start')
        for element in self.menu_ui:
            self.group.add(element)

    def _setup_trade_buttons(self, setup_type:str) ->None:
        """
        Configure ui buttons for starting or ending a trade situation.

        Args:
            setup_type(str): determines what buttons to take or give back to the systems.

                -"start": add buy and sell buttons, while removing the drop button

                -"end": remove buy and sell buttons, give back the drop button
        """
        if setup_type == 'start':
            for button in self.interactor.inventory_ui.sidebar.active_buttons:
                if button.name == 'Drop':
                    self.temp_buttons.append(button)
                    self.interactor.inventory_ui.sidebar.active_buttons.remove(button)
            self.interactor.inventory_ui.sidebar.active_buttons.append(self.sell_button)
            self.owner.inventory_ui.sidebar.active_buttons.append(self.buy_button)
        elif setup_type == 'end':
            self.interactor.inventory_ui.sidebar.active_buttons.remove(self.sell_button)
            self.interactor.inventory_ui.sidebar.active_buttons.extend(self.temp_buttons)
            self.owner.inventory_ui.sidebar.active_buttons.remove(self.buy_button)
            self.temp_buttons.clear()
        self.owner.inventory_ui.sidebar.update_buttons()
        self.interactor.inventory_ui.sidebar.update_buttons()

    def update(self, dt) -> None:
        self._update_text()
        self._input()
     
    def _input(self) -> None:
        self.mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        self._click_based_input()
        self._key_based_input(keys)

    def _key_based_input(self, keys) -> None:
        if not keys[pygame.K_b or pygame.K_RETURN or pygame.K_e or pygame.K_u or pygame.K_a or pygame.K_d]:
            self.key_pressed = False
        
        if not keys[pygame.K_LCTRL]:
            self.selecting_all_of_type = False

        if not self.key_pressed and keys[pygame.K_ESCAPE]:
            self.exit()
            self.key_pressed = True

        if not self.key_pressed and keys[pygame.K_LCTRL]:
            self.key_pressed = True
            self.selecting_all_of_type = True

        if keys[pygame.K_a] or keys[pygame.K_d]:
            self._ui_update()
            self.key_pressed = True

    def _click_based_input(self) -> None:
        #handle all click based interactions
        if not pygame.mouse.get_pressed()[0]:
            self.clicking = False

        for button in self.buttons:
            if button.rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
                button.click()

        #add items to carts    
        for item_slot in self.transactable_spaces:
            if item_slot.rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
                if item_slot.subject and not self.clicking:
                    if item_slot.subject in self.owner.inventory and not self.clicking and item_slot.subject not in self.buy_cart:
                        self.buy_cart.append(item_slot.subject)
                    elif item_slot.subject in self.interactor.inventory and not self.clicking and item_slot.subject not in self.sell_cart:
                        self.sell_cart.append(item_slot.subject)
                    elif item_slot.subject in self.sell_cart and not self.clicking:
                        self.sell_cart.remove(item_slot.subject)
                    elif item_slot.subject in self.buy_cart and not self.clicking:
                        self.buy_cart.remove(item_slot.subject)
                    self.clicking = True
                    self._ui_update()
    
    def _ui_update(self) -> None:
        self.owner.inventory_ui.menu_refresh()
        self.interactor.inventory_ui.menu_refresh()
        for slot in self.transactable_spaces:
            slot.click(toggle=0)
            if slot.subject in (self.sell_cart+self.buy_cart):
                slot.click()

    def _refresh(self) -> None:
        self._ui_update()
        self.sell_cart = []
        self.buy_cart = []

    def _sell(self) -> None: 
        #transact player inventory out, and into the shop inventory. then update the sprites
        if self.owner.gold >= sum(item.value for item in self.sell_cart):
            for item in self.sell_cart:
                self.owner.gold -= item.value
                self.interactor.gold += item.value
                self.interactor.inventory.remove(item)
                self.owner.inventory.insert(0,item)
        self._refresh()
            
    def _buy(self) -> None: 
        #transact player inventory out, and into the shop 
        if self.interactor.gold >= sum(item.value for item in self.buy_cart):
            for item in self.buy_cart:
                self.interactor.gold -= item.value
                self.owner.gold += item.value
                self.owner.inventory.remove(item)
                self.interactor.inventory.insert(0,item)
            self._refresh()

    def _update_text(self) -> None:
        #update any objects that have a dynamic text string that need to update once per frame. 
        sell_cart_value = sum(item.value for item in self.sell_cart)
        buy_cart_value = sum(item.value for item in self.buy_cart)
        cart_value = sell_cart_value - buy_cart_value
        self.gold_textbox.text = str(cart_value)
        error_message = 'Missing Funds'
        if int(cart_value) < 0 and self.interactor.gold - abs(int(cart_value)) < 0 :
            error_message = 'Missing Funds'
            self.gold_textbox.color = 'red'
            self.gold_textbox.text = error_message
        elif int(cart_value) == 0:
            self.gold_textbox.color = 'black'
        elif int(cart_value) < 0:
            self.gold_textbox.color = 'red'
        elif int(cart_value) > 0:
            self.gold_textbox.color = 'dark green'

    def exit(self) -> None:
        self.buy_cart.clear()
        self.sell_cart.clear()
        self._setup_trade_buttons('end')
        self.interactor.inventory_ui.exit()
        self.owner.inventory_ui.exit()
        self.is_active = False
        for element in self.menu_ui:
            self.group.remove(element)
