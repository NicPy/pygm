# `pos` is the `x,y` from `event.pos`
# x, y is the x/y co-ords from the x/y where you render a button
# x1, y1 is the width/height for the button.
# This function will return true if the button is clicked on.

def button_check(pos, x, y, x1, y1): 
    return pos[0] >= x and pos[0] < x + x1 and pos[1] >= y and pos[1] < y + y1

# This function will create a nice button with text in it.
# `sufrace` is like the default 'DISPLAYSURF', `color` is the color of the box
# `text_color` is the color of the text in the box
# `x/y` are the co-ords of the button. `width/height` are the dimensions of button
# `text` is the text for the label.

def make_button(surface,color,text_color,x,y,width,height,text):
    pygame.draw.rect(surface, (0,0,0),(x-1,y-1,width+2,height+2),1) #makes outline around the box
    pygame.draw.rect(surface, color,(x,y,width,height))#mkes the box

    myfont = pygame.font.SysFont('Arial Black', 15) #creates the font, size 15 (you can change this)
    label = myfont.render(text, 1, text_color) #creates the label
    surface.blit(label, (x+2, y)) #renders the label



#example of use:
menu_items = ['Play','Load','Volume','High Scores','Exit']
while True:
    for i in range(len(menu_items)-1):#goes through each item
        make_button(DISPLAYSURF,SILVER,BLACK,10,10+(20*i),120,menu_items[i]) #puts the item into the make_button, `+20*i` will make each item 15px down from the last.

    for event in pygame.event.get():
        if event.type == 5:
            if event.button == 1:
                for i in range(len(menu_items)-1):#check every button

                    if button_check(event.pos,10,10+(20*i),120):
                        if i == 0:
                            play()
                        elif i == 1:
                            load()
                        elif i == 4:
                            pygame.quit()
                            sys.exit()