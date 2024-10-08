package lab1_pack;

import static java.lang.Math.*;

import java.util.random.RandomGenerator;

public class lab1 {
    public static void arr(int str_arr[], double col_arr[], double arr_arr[][], int col, int str) { //статический метод для заполнения двумерного массива
        for (int i = 0; i < col; i++) {
            for (int j = 0; j < str; j++) {
                if (str_arr[i] == 7) {
                    arr_arr[i][j] = pow(pow((tan(col_arr[j]) / 2), 3), log(abs(col_arr[j])) * (cos(pow((2 * (1 - col_arr[j])), col_arr[j])) + 1));
                } else if (str_arr[i] == 9 || str_arr[i] == 11 || str_arr[i] == 15 || str_arr[i] == 19) {
                    arr_arr[i][j] = cbrt(atan(pow((col_arr[j] - 1.5) / 15, 2)));
                } else {
                    arr_arr[i][j] = pow(2 * (pow((pow(pow(E, col_arr[j]) - 0.5, 3)), (2 * 0.25 * (asin((col_arr[j] - 1.5) / 15) - 1)))), 3);
                }
            }
        }
    }

    public static void out(double arr_arr[][]) { //статический метод для вывода в консоль двумерного массива
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 20; j++) {
                if (j == 19) {
                    System.out.printf("%15.4f\n", arr_arr[i][j]);
                } else {
                    System.out.printf("%15.4f", arr_arr[i][j]);
                }
            }
        }
    }

    public static void main(String[] args) {
        int z_len = 9; //длина массива z
        int x_len = 20; //длина массива x

        int z[] = new int[z_len]; //создание массива z
        double x[] = new double[x_len]; //создание массива x
        double z1[][] = new double[z_len][x_len]; //создание двумерного массива z1

        int k = 0; //индекс для заполнения массива z
        for (int i = 5; i <= 21; i += 2) { //заполнение массива z нечетными числами от 5 до 21 включительно
            z[k] = i;
            k++;
        }
        for (int i = 0; i < x_len; i++) { //заполнение массива x случайными значениями в диапазоне от -9.0 включительно до 6.0 невключительно
            x[i] = RandomGenerator.getDefault().nextInt(-9, 6); //автоматически переводит числа из тип int в double
        }

        arr(z, x, z1, z_len, x_len); //считаем значения
        out(z1); //выводим значения
    }
}
