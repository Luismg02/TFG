#include <linux/module.h>
#include <linux/kernel.h> // __FUNCTION__
#include <linux/init.h>
#include <linux/slab.h> // kmalloc kfree

MODULE_LICENSE("GPL");

static int __init test_init(void)
 {
        char *buf = kmalloc(10, GFP_KERNEL);
        kfree(buf);
        printk(KERN_INFO "buf: %c\n", *buf);
        return 0;
 }


static void __exit test_exit(void)
{
    printk("%s removed.\n",__func__);

}

module_init(test_init);
module_exit(test_exit);
