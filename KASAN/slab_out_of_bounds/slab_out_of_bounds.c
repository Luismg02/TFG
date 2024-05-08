#include <linux/module.h>
#include <linux/kallsyms.h>
#include <asm/uaccess.h>
#include <linux/syscalls.h>
#include <linux/kernel.h> // __FUNCTION__
#include <linux/slab.h> // kmalloc kfree

MODULE_LICENSE("GPL");

static int __init test_init(void)
 {
        char *ptr;
        size_t size = 124;

        pr_info("out-of-bounds to right\n");
        ptr = kmalloc(size, GFP_KERNEL);
        if (!ptr) {
                pr_err("Allocation failed\n");
                return 0;
        }
        pr_info("ptr address: 0x%lx\n", ptr);

        ptr[size] = 'x';
        pr_info("ptr[size] address: 0x%lx\n", ptr + size);

        kfree(ptr);
        return 0;
 }


static void __exit test_exit(void)
{
    printk("%s removed.\n",__func__);

}

module_init(test_init);
module_exit(test_exit);
