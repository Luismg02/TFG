obj-m += user_memory_access.o

EXTRA_CFLAGS += -g -Wall

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules


clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
