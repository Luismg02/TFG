#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");

void vulnerable_function(void) {
    char buffer[10];
    const char *source = "Vamos a desbordar ese buffer jajajaja";
    char *destination = buffer;

    // Utilizar escritura directa para provocar desbordamiento
    while (*source != '\0') {
        *destination = *source;
        destination++;
        source++;
    }
}

static int __init buffer_overflow_init(void) {
    printk(KERN_INFO "Inicializando módulo de kernel\n");
    vulnerable_function();
    return 0;
}

static void __exit buffer_overflow_exit(void) {
    printk(KERN_INFO "Saliendo del módulo de kernel\n");
}

module_init(buffer_overflow_init);
module_exit(buffer_overflow_exit);
