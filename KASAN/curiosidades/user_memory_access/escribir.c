#include <stdio.h>
#include <stdlib.h>

int main() {
    // Tamaño de memoria a asignar en bytes
    size_t size = 1024;

    // Asignar memoria dinámicamente
    void *ptr = malloc(size);

    if (ptr == NULL) {
        fprintf(stderr, "No se pudo asignar memoria.\n");
        return 1;
    }

    printf("Dirección de memoria asignada: %p\n", ptr);

    // No se libera la memoria cuando ya no se necesita

    return 0;
}
