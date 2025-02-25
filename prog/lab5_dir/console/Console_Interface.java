package console;

import java.util.Scanner;

public interface Console_Interface {
    void print(Object o);
    void println(Object o);
    void printError(Object o);
    void printTable(Object o1, Object o2);
    boolean canReadln();
    String readln();
    void prompt();
    String getPrompt();
    void selectFileScanner(Scanner o);
    void selectConsoleScanner();
}
