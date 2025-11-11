#include <iostream>
#include <thread>
#include <chrono>

int main() {
    for (int i = 1; i <= 5; i++) {
        std::cout << "C++: строка " << i << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
    return 0;
}
