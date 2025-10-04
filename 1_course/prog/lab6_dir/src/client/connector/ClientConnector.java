package client.connector;

import common.console.Console;
import common.packing.Answer;
import common.packing.Container;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.PortUnreachableException;
import java.net.SocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.DatagramChannel;

/**
 * Класс для управления сетевым взаимодействием клиента с сервером через UDP.
 * Обеспечивает отправку и получение сериализованных объектов Container.
 */
public class ClientConnector {
    private DatagramChannel channel;
    private final InetSocketAddress serverAddress;
    private final Console console;

    /**
     * Конструктор ClientConnector.
     * @param host хост сервера
     * @param port порт сервера
     * @param console консоль для вывода сообщений
     */
    public ClientConnector(String host, int port, Console console) {
        this.serverAddress = new InetSocketAddress(host, port);
        this.console = console;
    }

    /**
     * Инициализирует подключение к серверу.
     * @return результат подключения (Answer)
     */
    public Answer init() {
        try {
            channel = DatagramChannel.open();
            channel.connect(serverAddress);
            return new Answer("Подключение установлено", true);
        } catch (IOException e) {
            return new Answer("Ошибка подключения: " + e.getMessage(), false);
        }
    }

    /**
     * Отправляет контейнер на сервер и получает ответ.
     * @param container контейнер с данными
     * @return ответ сервера (Answer)
     */
    public Answer send(Container container) {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(container);
            byte[] data = baos.toByteArray();

            ByteBuffer buffer = ByteBuffer.wrap(data);
            channel.write(buffer);

            ByteBuffer responseBuffer = ByteBuffer.allocate(65507);
            int bytesRead = channel.read(responseBuffer);

            if (bytesRead > 0) {
                responseBuffer.flip();
                ObjectInputStream ois = new ObjectInputStream(
                        new ByteArrayInputStream(responseBuffer.array()));
                Container response = (Container) ois.readObject();

                if (response.getAnswer().message().equalsIgnoreCase("exit")) {
                    channel.close();
                    System.exit(0);
                }
                return response.getAnswer();
            } else {
                return new Answer("Не получен ответ от сервера", false);
            }
        } catch (PortUnreachableException e) {
            return new Answer("Сервер временно недоступен", false);
        } catch (IOException | ClassNotFoundException e) {
            return new Answer("Ошибка отправки: " + e.getMessage(), false);
        }
    }

    /**
     * Возвращает локальный адрес клиента.
     * @return SocketAddress или null при ошибке
     */
    public SocketAddress getAddress() {
        try {
            return channel.getLocalAddress();
        } catch (IOException e) {
            return null;
        }
    }
}
