package console;

import java.util.NoSuchElementException;
import java.lang.IllegalStateException;
import java.util.Scanner;

/**
 * Класс для взаимодействия с пользователем через консоль.
 * Поддерживает ввод данных как с консоли, так и из файла.
 */
public class Console {

    /** Приглашение для ввода. */
    private static final String P = "> ";

    /** Сканер для чтения данных из файла. */
    private static Scanner fileScanner = null;

    /** Сканер для чтения данных с консоли. */
    private static Scanner defScanner = new Scanner(System.in);

    /**
     * Выводит объект в консоль.
     *
     * @param o объект для вывода
     */
    public void print(Object o) {
        System.out.print(o);
    }

    /**
     * Выводит объект в консоль с переходом на новую строку.
     *
     * @param o объект для вывода
     */
    public void println(Object o) {
        System.out.println(o);
    }

    /**
     * Выводит сообщение об ошибке в консоль.
     *
     * @param o сообщение об ошибке
     */
    public void printError(Object o) {
        System.out.println("Error: " + o);
    }

    /**
     * Форматированный вывод данных в виде таблицы.
     *
     * @param o1 первый объект для вывода
     * @param o2 второй объект для вывода
     */
    public void printTable(Object o1, Object o2) {
        System.out.printf(" %-56s%-1s%n", o1, o2);
    }

    /**
     * Проверяет, доступна ли следующая строка для чтения.
     *
     * @return true, если доступна следующая строка, иначе false
     * @throws IllegalStateException если сканер закрыт
     */
    public boolean canReadln() throws IllegalStateException {
        if (fileScanner != null) {
            return fileScanner.hasNextLine();
        } else {
            return defScanner.hasNextLine();
        }
    }

    /**
     * Читает следующую строку из текущего источника (файл или консоль).
     *
     * @return прочитанная строка
     * @throws NoSuchElementException если строка отсутствует
     * @throws IllegalStateException если сканер закрыт
     */
    public String readln() throws NoSuchElementException, IllegalStateException {
        if (fileScanner != null) {
            return fileScanner.nextLine();
        } else {
            return defScanner.nextLine();
        }
    }

    /**
     * Выводит приглашение для ввода.
     */
    public void prompt() {
        print(P);
    }

    /**
     * Возвращает текущее приглашение для ввода.
     *
     * @return приглашение для ввода
     */
    public String getPrompt() {
        return P;
    }

    /**
     * Переключает сканер на чтение из файла.
     *
     * @param o сканер для чтения из файла
     */
    public void selectFileScanner(Scanner o) {
        Console.fileScanner = o;
    }

    /**
     * Переключает сканер на чтение с консоли.
     */
    public void selectConsoleScanner() {
        Console.fileScanner = null;
    }
}