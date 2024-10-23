from pygame.math import Vector2

#screen settings
screen_width = 1200
screen_height = 600
screen_color = (30,30,60)

#player settings
player_speed = 100

#dialoge settings
TEXT_SPEED = 25

#drawing layers
cameragroup_layers = {
    'ocean': 10,
    'overworld': 20,
    'events': 30,
    'main': 40,
    'overlay+': 45,
    'hud': 50,
    'items': 60,
    'text': 70
}
overlay_layers = {
    'hud': 10,
    'hud_elements': 20,
    'menu': 30,
    'menu_aux': 35,
    'menu_elements': 40,
    'menu_items': 50,
    'text': 60
}

#weather setup
weather_type = {
        'sunny': {
                 'sky_color': [173, 216, 230],
                 'min_cloud_count': 0,
                 'max_cloud_count': 8,
                 'min_wave_count': 10,
                 'max_wave_count': 20
                 },

        'cloudy':{
                'sky_color': [83, 146, 170],
                'min_cloud_count': 8,
                'max_cloud_count': 13,
                'min_wave_count': 10,
                'max_wave_count': 20
                },

        'overcast' : {
            'sky_color': [90, 90, 90], 
            'min_cloud_count': 8,  
            'max_cloud_count': 15,
            'min_wave_count': 15,
            'max_wave_count': 30
            },

        'rainy' : {
            'sky_color': [90, 90, 90], 
            'min_cloud_count': 10,  
            'max_cloud_count': 20,
            'min_wave_count': 25,
            'max_wave_count': 50
            },

        'windy' : {
            'sky_color': [53, 125, 170],  
            'min_cloud_count': 0, 
            'max_cloud_count': 25,
            'min_wave_count': 25,
            'max_wave_count': 50
            }
}

def swap(var1, var2):
    temp_var = var1
    var1 = var2
    var2 = temp_var
    return(var1, var2)