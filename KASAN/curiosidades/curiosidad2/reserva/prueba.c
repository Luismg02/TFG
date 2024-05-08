#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/slab.h>

// Función de inicialización del módulo
static int __init mi_modulo_init(void) {
    void *mi_puntero;

    // Reservamos 100 bytes de memoria
    mi_puntero = kmalloc(100, GFP_KERNEL);

    if (mi_puntero == NULL) {
        // Manejo el error si la asignación de memoria falla
        printk(KERN_ERR "Error al asignar memoria con kmalloc\n");
        return -ENOMEM; // Informo al kernel que hubo un error durante la inicialización
    }

    // Imprimo la dirección de memoria
    pr_info("Dirección de memoria asignada: %p\n", mi_puntero);

    return 0; // El módulo se cargó con éxito
}

// Función de limpieza del módulo
static void __exit mi_modulo_exit(void) {
    pr_info("Saliendo del módulo\n");
}

//Funciones de inicialización y limpieza del módulo
module_init(mi_modulo_init);
module_exit(mi_modulo_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Ejemplo de módulo de kernel con kmalloc");
