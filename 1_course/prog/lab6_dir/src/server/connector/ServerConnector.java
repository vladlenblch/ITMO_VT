package server.connector;

import common.packing.Answer;
import common.packing.Container;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.*;
import java.net.*;

/**
 * Класс Connector для работы с UDP соединениями
 * Обеспечивает прием и отправку сериализованных объектов через DatagramSocket
 */
public class ServerConnector {
    private static final Logger logger = LogManager.getLogger(ServerConnector.class);

    private DatagramSocket socket;
    private int port;
    private byte[] buffer = new byte[65507];
    private InetAddress inetAddress;
    private int userPort;

    /**
     * Конструктор ServerConnector
     * @param port порт для прослушивания входящих соединений
     */
    public ServerConnector(int port) {
        this.port = port;
    }

    /**
     * Запускает сервер и начинает прослушивание указанного порта
     * @return Answer с результатом операции
     */
    public Answer startPolling() {
        if (port < 0 || port > 65535) {
            logger.error("Попытка использования недопустимого порта: {}", port);
            return new Answer("Ошибка: неверный порт", false);
        }
        try {
            socket = new DatagramSocket(port);
            socket.setSoTimeout(5000);
            logger.info("Сервер успешно запущен на порту {}", port);
            return new Answer("Сервер запущен на порту " + port, true);
        } catch (SocketException e) {
            logger.error("Ошибка инициализации сокета на порту {}: {}", port, e.getMessage());
            return new Answer("Ошибка запуска: " + e.getMessage(), false);
        }
    }

    /**
     * Получает входящий запрос от клиента
     * @return Container с данными запроса или null при ошибке/таймауте
     */
    public Container getRequest() {
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
        try {
            socket.receive(packet);
            inetAddress = packet.getAddress();
            userPort = packet.getPort();

            try (ObjectInputStream ois = new ObjectInputStream(
                    new ByteArrayInputStream(packet.getData(), 0, packet.getLength()))) {

                Container receivedObject = (Container) ois.readObject();
                if (receivedObject != null) {
                    logger.info("Получен запрос от {}:{}", inetAddress.getHostAddress(), userPort);
                }
                return receivedObject;
            }
        } catch (SocketTimeoutException e) {
            logger.debug("Таймаут при ожидании запроса");
            return null;
        } catch (IOException | ClassNotFoundException e) {
            logger.warn("Ошибка получения запроса: {}", e.getMessage());
            return null;
        }
    }

    /**
     * Отправляет ответ клиенту
     * @param container контейнер с данными для отправки
     * @return Answer с результатом операции отправки
     */
    public Answer sendPacket(Container container) {
        if (container == null) {
            logger.warn("Попытка отправки null-контейнера");
            return new Answer("Ошибка: пустые данные для отправки", false);
        }

        if (inetAddress == null || userPort == 0) {
            logger.warn("Попытка отправки без установленного адреса клиента");
            return new Answer("Ошибка: адрес клиента не установлен", false);
        }

        try (ByteArrayOutputStream baos = new ByteArrayOutputStream();
             ObjectOutputStream oos = new ObjectOutputStream(baos)) {

            oos.writeObject(container);
            byte[] data = baos.toByteArray();
            DatagramPacket responsePacket = new DatagramPacket(
                    data, data.length, inetAddress, userPort);

            socket.send(responsePacket);
            logger.info("Ответ успешно отправлен на {}:{}",
                    inetAddress.getHostAddress(), userPort);
            return new Answer("Данные отправлены", true);
        } catch (IOException e) {
            logger.error("Ошибка отправки ответа на {}:{}: {}",
                    inetAddress.getHostAddress(), userPort, e.getMessage());
            return new Answer("Ошибка отправки: " + e.getMessage(), false);
        }
    }
}