#include <stdio.h>
#include <stdlib.h>

void encrypt(char* text, int key) {
    for (int i = 0; text[i] != '\0'; i++) {
        if (text[i] >= 'a' && text[i] <= 'z') {
            text[i] = 'a' + (text[i] - 'a' + key) % 26;
        } else if (text[i] >= 'A' && text[i] <= 'Z') {
            text[i] = 'A' + (text[i] - 'A' + key) % 26;
        }
    }
}

void decrypt(char* text, int key) {
    for (int i = 0; text[i] != '\0'; i++) {
        if (text[i] >= 'a' && text[i] <= 'z') {
            text[i] = 'a' + (text[i] - 'a' - key + 26) % 26;
        } else if (text[i] >= 'A' && text[i] <= 'Z') {
            text[i] = 'A' + (text[i] - 'A' - key + 26) % 26;
        }
    }
}

int main(int argc, char* argv[]) {
    char* text = argv[1];
    int key = atoi(argv[2]);

    printf("original string  : %s\n", text);
    printf("key              : %d\n", key);

    encrypt(text, key);
    printf("encrypted string : %s\n", text);

    decrypt(text, key);
    printf("decrypted string : %s\n", text);

    return 0;
}
