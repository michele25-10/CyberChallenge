#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

int main()
{
    // Ora è un array da 40 byte, come serve
    uint8_t var_88[40] = {0};
    memcpy(var_88, "\xe3\xe9\xf1\xf2\xf8\xec\xfb\xe8\xf1\xc1\xec\xfb\xf8\xf8\xeb\xfc\xc1\xf1\xea\xc1\xfb\xe8\xf7\xf2\xc1\xf9\xf0\xf1\xf2\xe5\xd9\xdf\xd2\xd8\x00\x00\x00\x00\x00\x00", 0x28);

    // Area di lavoro temporanea, non usata nel codice ma lasciata per coerenza
    uint8_t s[60] = {0};
    memset(s, 0, 60);

    int32_t var_c = 0;

    // Conta la lunghezza della stringa (fino a \0)
    while (var_88[var_c])
        var_c += 1;

    // Reverse della stringa
    for (int32_t i = 0; i < (var_c + (var_c >> 31)) >> 1; i++)
    {
        uint8_t tmp = var_88[i];
        var_88[i] = var_88[var_c - i - 1];
        var_88[var_c - i - 1] = tmp;
    }

    // XOR con 0x61
    for (int32_t i = 0; i < var_c; i++)
        var_88[i] ^= 0x61;

    // NOT bitwise
    for (int32_t i = 0; i < var_c; i++)
        var_88[i] = ~var_88[i];

    // Stampa risultato
    for (int32_t i = 0; i < var_c; i++)
        putchar(var_88[i]);

    return 0;
}
