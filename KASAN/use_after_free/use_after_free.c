#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gfp.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");

static unsigned long *page_ptr;

static int __init test_init(void)
{
    pr_info("use-after-free example without kmalloc/vmalloc/kfree\n");

    // Asignar una página de memoria física con __get_free_pages
    unsigned long page = __get_free_pages(GFP_KERNEL, 0);
    if (!page) {
        pr_err("Allocation failed\n");
        return -ENOMEM;
    }
    page_ptr = (unsigned long *)page;

    pr_info("page_ptr address: 0x%lx\n", (unsigned long)page_ptr);

    // Liberar la página de memoria con free_pages
    free_pages((unsigned long)page_ptr, 0);
    //Intentar acceder a la memoria liberada (use-after-free)
    pr_info("Accessing memory after free: %lu\n", *page_ptr);

    
    return 0;
}

static void __exit test_exit(void)
{
    pr_info("%s removed.\n", __func__);
}

module_init(test_init);
module_exit(test_exit);
