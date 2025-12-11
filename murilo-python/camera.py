import cv2
import argparse
import time
if not cap.isOpened():
 raise SystemExit(f"Não foi possível abrir a câmera {args.camera}")
 
args = parser.parse_args()
cap = cv2.VideoCapture(args.camera)
# Força resolução (algumas câmeras ignoram se não suportarem)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
cap.set(cv2.CAP_PROP_FPS, args.fps)


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = None
recording = True # inicia gravando — troque para False se preferir começar sem gravar


print('Pressione r para alternar gravação, q para sair.')


while True:
    ret, frame = cap.read()
    if not ret:
        print('Frame não recebido — encerrando')
        break


    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2


    # desenha mira: linhas horizontais e verticais com gap central
    x1 = cx - args.length
    x2 = cx + args.length
    y1 = cy - args.length
    y2 = cy + args.length


    # linha horizontal esquerda
    cv2.line(frame, (x1, cy), (cx - args.gap, cy), (0, 255, 0), args.thickness)
    # linha horizontal direita
    cv2.line(frame, (cx + args.gap, cy), (x2, cy), (0, 255, 0), args.thickness)
    # linha vertical cima
    cv2.line(frame, (cx, y1), (cx, cy - args.gap), (0, 255, 0), args.thickness)
    # linha vertical baixo
    cv2.line(frame, (cx, cy + args.gap), (cx, y2), (0, 255, 0), args.thickness)


    # pequeno círculo central opcional
    if args.circle:
     cv2.circle(frame, (cx, cy), max(2, args.thickness * 2), (0, 255, 0), -1)


    # legendas de estado
    status_text = f"GRAVANDO" if recording else "PAUSADO"
    cv2.putText(frame, status_text, (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


    # inicializa writer quando começar a gravar
    if recording and writer is None:
     writer = cv2.VideoWriter(args.output, fourcc, args.fps, (w, h))
    start_time = time.time()
    print(f'Gravando em {args.output} ...')


# escreve frame se estiver gravando
if recording and writer is not None:
    writer.write(frame)


cv2.imshow('Webcam - Mira', frame)


key = cv2.waitKey(1) & 0xFF
if key == ord('q'):
    exit
elif key == ord('r'):
    recording = not recording
if not recording:
 print('Gravação pausada')
else:
 print('Gravação retomada')


# limpeza
cap.release()
if writer is not None:
    writer.release()
cv2.destroyAllWindows()
print('Encerrado')