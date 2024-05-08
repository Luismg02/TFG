#include <linux/module.h>
#include <linux/kernel.h>

static int test_init(void) {
    // Dirección de memoria
    int *ptr = (int *)0x0000000075184aed;

    // Leer desde la posición de memoria
    int value = *ptr;

    // Imprimir el valor leído
    printk(KERN_INFO "Valor leído desde la dirección de memoria: %d\n", value);

    return 0;
}

static void test_exit(void) {
    printk(KERN_INFO "Módulo de kernel desinstalado.\n");
}

module_init(test_init);
module_exit(test_exit);

MODULE_LICENSE("GPL");
