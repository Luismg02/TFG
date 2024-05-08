#include <linux/module.h>
#include <linux/kernel.h> // __FUNCTION__
#include <linux/slab.h> // kmalloc kfree

MODULE_LICENSE("GPL");

static int __init test_init(void)
 {
        int *ptr = (int *)0x12345678;

        pr_info("USER MEMORY ACCESS\n");
        printk("*ptr = %d\n", *ptr);
        return 0;
 }


static void __exit test_exit(void)
{
    printk("%s removed.\n",__func__);

}

module_init(test_init);
module_exit(test_exit);
