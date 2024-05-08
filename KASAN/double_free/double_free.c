#include <linux/module.h>
//#include <linux/kallsyms.h>
//#include <asm/uaccess.h>
//#include <linux/syscalls.h>
#include <linux/kernel.h> // __FUNCTION__
#include <linux/slab.h> // kmalloc kfree

MODULE_LICENSE("GPL");

static int __init test_init(void)
 {
        int *p = kmalloc(sizeof(int), GFP_KERNEL);

        *p = 42;

        pr_info("DOUBLE FREE\n");
        printk(KERN_INFO "El valor de p es %d\n", *p);

        kfree(p);
        kfree(p);
        
        return 0;
 }


static void __exit test_exit(void)
{
    printk("%s MODULO DESCARGADO\n",__func__);

}

module_init(test_init);
module_exit(test_exit);
