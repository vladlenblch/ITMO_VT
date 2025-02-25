package console;

import java.util.NoSuchElementException;
import java.lang.IllegalStateException;
import java.util.Scanner;

public class Console implements Console_Interface {
    private static final String P = "$ ";
    private static Scanner fileScanner = null;
    private static Scanner defScanner = new Scanner(System.in);

    public void print(Object o) {
        System.out.print(o);
    }

    public void println(Object o) {
        System.out.println(o);
    }

    public void printError(Object o) {
        System.out.println("Error: " + o);
    }

    public void printTable(Object o1, Object o2) {
        System.out.printf(" %-65s%-1s%n", o1, o2);
    }

    public boolean canReadln() throws IllegalStateException {
        if (fileScanner != null) {
            return fileScanner.hasNextLine();
        } else {
            return defScanner.hasNextLine();
        }
    }
    
    public String readln() throws NoSuchElementException, IllegalStateException {
        if (fileScanner != null) {
            return fileScanner.nextLine();
        } else {
            return defScanner.nextLine();
        }
    }

    public void prompt() {
        print(P);
    }

    public String getPrompt() {
        return P;
    }

    public void selectFileScanner(Scanner o) {
        Console.fileScanner = o;
    }

    public void selectConsoleScanner() {
        Console.fileScanner = null;
    }
}
