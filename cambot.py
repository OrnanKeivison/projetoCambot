import cv2
import numpy as np
import serial
import json
import time

def detectarVitimas(cam):
    # Lê um quadro do vídeo
    ret, frame = cam.read()

    # Verifica se o vídeo foi lido corretamente
    if not ret:
        print("Erro ao ler o vídeo.")
        return []

    # Converte o quadro para escala de cinza
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplica desfoque para reduzir ruídos
    img_blur = cv2.medianBlur(img_gray, 5)

    # Detecta círculos usando a Transformada de Hough
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, dp=1, minDist=70, param1=70, param2=35, minRadius=40, maxRadius=0)
    
    circuloDetectado = {"x": 0, "y": 0, "r": 0, "s": " "}
    # Verifica se algum círculo foi detectado
    if circles is not None:
        circles = np.uint16(np.around(circles))

        i = circles[0, 0]
        
        # Extrai as coordenadas do centro e o raio do círculo
        x, y, radius = i[0], i[1], i[2]

        # Converte a imagem para o espaço de cor HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Obtém o valor médio da região central do círculo
        circle_region = hsv[y - radius:y + radius, x - radius:x + radius]
        
        # Calcula a média do canal V (brilho) da região
        avg_v = np.mean(circle_region[:, :, 2])

        # Se a média do valor (V) for baixa, indica uma cor escura (preta)
        if avg_v < 70:  # Limiar de intensidade para considerar "preto"
            status = 'dead'
        else:
            status = 'alive'

        # Adiciona as coordenadas à lista de círculos detectados
        circuloDetectado = {"x": int(((x-320)*5)/16), "y": int(y), "r": int(radius), "s": status}

    return circuloDetectado


#função para envio de dados para o arduino
def enviarIno(circulo, ser):
    vitima = json.dumps(circulo)
    
    
    ser.write(vitima.encode('utf-8'))



# Execução do script

# Inicializa a câmera
cap = cv2.VideoCapture(0)
# Inicializa a porta serial
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)


# Loop para capturar e processar os quadros do vídeo
while True:
    mensagem = ser.readline().decode('utf-8').strip()
    print(mensagem)
    
    if mensagem == 'get':
        
        # Detecta círculos na imagem capturada
        circulo = detectarVitimas(cap)
        
        # Exibe a imagem com os círculos detectados
        if circulo:
            print(f"raspy: {circulo}")
            enviarIno(circulo, ser)

