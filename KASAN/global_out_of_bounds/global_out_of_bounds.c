#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");

int my_array[5];
int i;

static int __init my_module_init(void) {

    pr_info("Initializing my_module\n");

    // Accessing array elements within bounds
    for (i = 0; i < 5; i++) {
        my_array[i] = i;
    }

    // Accessing an element out of bounds
    pr_info("Accessing an element out of bounds: %d\n", my_array[5]);

    return 0;
}

static void __exit my_module_exit(void) {
    pr_info("Exiting my_module\n");
}

module_init(my_module_init);
module_exit(my_module_exit);
