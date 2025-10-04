package server.commands;

import common.packing.Answer;

/**
 * Интерфейс, предназначенный для исполнения
 */
public interface Executable {
    Answer execute(String arguments);
}
