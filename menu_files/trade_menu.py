import pygame
from sprite_files.hud import UiButton
from sprite_files.sprites import Textbox, Generic
from SETTINGS import *


class TradeMenu(pygame.sprite.Sprite):
    def __init__(self, group, owner) -> None:
        super().__init__(group)
        self.group= group
        self.is_active = False
        self.buy_cart = []
        self.sell_cart = []
        self.z = overlay_layers['menu']
        self.owner = owner
        self._menu_setup()
        self.group.remove(element for element in self.menu_ui)  #remove from group to prevent from rendering.

    def _menu_setup(self) -> None:
        """set the position for each element of the menu and assign its logic"""
        #menu setup
        self.image = pygame.image.load('images/hud/shop_bar.png')
        self.rect = self.image.get_rect(centerx=screen_width/2, bottom=screen_height)

        #items to display setup
        self.buy_button_image = pygame.image.load('images/hud/buy_button.png')
        self.sell_button_image = pygame.image.load('images/hud/sell_button.png')
        self.exit_button_image = pygame.image.load('images/hud/exit_button.png')
        self.buy_button = UiButton(self.group, self.buy_button_image, self.rect, (403,22))
        self.sell_button = UiButton(self.group, self.sell_button_image, self.rect, (39,22))
        self.exit_button = UiButton(self.group, self.exit_button_image, self.rect, (211, 13))
        self.gold_textbox = Textbox(self.group, self, offset=(239, 55))
        self.menu_ui = [self, self.gold_textbox, self.buy_button, self.sell_button, self.exit_button]

    def show_menu(self, interactor) -> None:
        self.interactor = interactor
        self.transactable_spaces = []
        self.transactable_spaces.extend(self.owner.inventory_ui.inventory_slots.values())
        self.transactable_spaces.extend(self.owner.inventory_ui.crew_slots.values())        
        self.transactable_spaces.extend(self.interactor.inventory_ui.inventory_slots.values())
        self.transactable_spaces.extend(self.interactor.inventory_ui.crew_slots.values())
        for element in self.menu_ui:
            self.group.add(element)

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

        if pygame.mouse.get_pressed()[0] and self.exit_button.rect.collidepoint(self.mouse_pos):
            self.exit()

        if (pygame.mouse.get_pressed()[0] and self.sell_button.rect.collidepoint(self.mouse_pos)):
            self._sell()
        
        if (pygame.mouse.get_pressed()[0] and self.buy_button.rect.collidepoint(self.mouse_pos)):
            self._buy()

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
        self.interactor.inventory_ui.exit()
        self.owner.inventory_ui.exit()
        self.is_active = False
        for element in self.menu_ui:
            self.group.remove(element)