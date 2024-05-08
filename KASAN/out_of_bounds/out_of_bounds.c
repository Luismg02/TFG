#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Luis Miguel");
MODULE_DESCRIPTION("Ejemplo de out_of_bounds KASAN");

static int __init test_init(void) {
    unsigned long *ptr = (unsigned long *)0xFFFFFFFFFFFFFFFFUL;  // Dirección de memoria no existente

    // Intento de acceso a la dirección de memoria
    printk(KERN_INFO "Valor en la dirección prohibida: %lx\n", *ptr);

    return 0;
}

static void __exit test_exit(void) {
    printk(KERN_INFO "Módulo descargado\n");
}

module_init(test_init);
module_exit(test_exit);
