import cv2
import numpy as np

def detectarCirculosImagem(video):
    # Lê um quadro do vídeo
    ret, frame = video.read()

    # Verifica se o vídeo foi lido corretamente
    if not ret:
        print("Erro ao ler o vídeo.")
        return []

    # Converte o quadro para escala de cinza
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplica desfoque para reduzir ruídos
    img_blur = cv2.medianBlur(img_gray, 5)

    # Detecta círculos usando a Transformada de Hough
    circles = cv2.HoughCircles(img_blur, 
                               cv2.HOUGH_GRADIENT, 
                               dp=1, 
                               minDist=70, 
                               param1=70, 
                               param2=35, 
                               minRadius=10, 
                               maxRadius=0)

    # Lista para armazenar os círculos detectados
    circulos_detectados = []

    # Verifica se algum círculo foi detectado
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            # Extrai as coordenadas do centro e o raio do círculo
            x, y, radius = i[0], i[1], i[2]

            # Converte a imagem para o espaço de cor HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Obtém o valor médio da região central do círculo
            circle_region = hsv[y - radius:y + radius, x - radius:x + radius]
            
            # Calcula a média do canal V (brilho) da região
            avg_v = np.mean(circle_region[:, :, 2])

            # Se a média do valor (V) for baixa, indica uma cor escura (preta)
            if avg_v < 60:  # Limiar de intensidade para considerar "preto"
                cor_circulo = (0, 0, 255)  # Vermelho
            else:
                cor_circulo = (0, 255, 0)  # Verde

            # Desenha o círculo em volta da esfera
            cv2.circle(frame, (x, y), radius, cor_circulo, 2)  # Círculo em torno da esfera

            # Marca o centro da esfera
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

            # Adiciona as coordenadas à lista de círculos detectados
            circulos_detectados.append({"x": x, "y": y, "radius": radius, "cor": cor_circulo})

    return circulos_detectados, frame


# Execução do script

# Inicializa a câmera
cap = cv2.VideoCapture(0)

# Loop para capturar e processar os quadros do vídeo
while True:
    # Detecta círculos na imagem capturada
    circulos, frame = detectarCirculosImagem(cap)

    # Exibe a imagem com os círculos detectados
    cv2.imshow('Detecção de Círculos', frame)

    # Exibe as coordenadas dos círculos detectados (opcional)
    if circulos:
        for circulo in circulos:
            print(f"Círculo detectado: {circulo}")

    # Verifica se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos da câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()