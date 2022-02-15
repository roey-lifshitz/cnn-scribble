import pygame
from canvas import Canvas
from mouse import Mouse
from Ui.Button import Button
from FileParser import FileParser
from NeuralNetwork import NeuralNetwork
from matplotlib import pyplot as plt
from Layers.Convolutional import Convolutional
from Layers.Pooling import Pooling
from Layers.Dense import Dense
from Layers.Flatten import Flatten
from Layers.Activations import Relu, Softmax
import cnn_numpy_sg as cnn

def main():
 
    pygame.font.init()
    background_colour = (255, 255, 255)
    (width, height) = (600, 600)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    canvas = Canvas(screen, 0, 0, 500, 500)
    mouse = Mouse(pygame.mouse.get_pos(), 2)
    file_parser = FileParser()
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=1000, test_amount=100)



    idx = 0
    network = NeuralNetwork()
    network.initialize([
        Convolutional(filters_num=8, filter_size=5),
        Relu(),
        Pooling(filter_size=2, stride=2),
        Convolutional(filters_num=16, filter_size=5),
        Relu(),
        Pooling(filter_size=2, stride=2),
        Flatten(),
        Dense(4),
        Softmax()
    ])
    network.train(train_x, train_y, test_x, test_y)
    network.save("Models/first.pkl")

    # Adding buttons to the screen
    img = pygame.image.load("images/eraser.png")
    buttons = [
        Button((540, 550, 50, 40), image=img, on_click=canvas.clear),
        Button((540, 500, 50, 40), text="show", on_click=canvas.get_data)
    ]
     #b3 = Button((540, 450, 50, 40), text="load", on_click=lambda: canvas.draw_loaded_data(train_x[idx], 2))

    #buttons.append(b3)


    running = True
    while running:
        mouse.pos = pygame.mouse.get_pos()

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    idx += 1
                    if idx == 24: idx = 0

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False
                mouse.prev_pos = None
                canvas.append_line()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True

                for button in buttons:
                    if button.on_click():
                        pass

            elif event.type == pygame.MOUSEMOTION:
                if mouse.pressed:
                    if canvas.contains(*mouse.pos) and mouse.prev_pos is not None:
                        canvas.draw_line(mouse.prev_pos, mouse.pos, mouse.radius)
                    mouse.prev_pos = mouse.pos

            if not mouse.pressed:
                for button in buttons:
                    if button.is_click(mouse.pos):
                        pass

        pygame.display.flip()


if __name__ == '__main__':
   main()

   """"
      
   """

   """
               The Neural Network will consist of the following Layers
               1. Convolutional Layer
               2. Max Pooling Layer
               3  Convolutional Layer
               4. Max Pooling Layer
               5. Flatter Layer
               6. Softmax Activation Layer
               
               net = cnn.Network([
        cnn.ConvLayer(32, 5),
        cnn.PoolLayer_Max(2, 2),
        cnn.ConvLayer(64, 5),
        cnn.PoolLayer_Max(2, 2),
        cnn.FlatLayer(),
        cnn.FCLayer_ReLU(512),
        cnn.FCLayer_ReLU(128),
        cnn.FCLayer_Softmax(4)
    ])

    for i in range(1000):
        for x, y, in zip(train_x, train_y):
            _, a, b = net.train(x, y, 0.01)
        print(a, i)
   """