#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

void post(int i, char* p)
{
    printf("Test %d: %s\n",i, p);
    memset(p, 0, 1024);
}

int main()
{
    int fd = -1;
    char *buffer = (char*)malloc(1024);
    memset(buffer, 0, 1024);

    fd = open("/dev/pa3_char_driver", O_RDWR);
    if (fd == -1) {
        perror("Failed to open the device");
        return 1;
    }

    // Test 1
    // expected: user space!
    write(fd, "Hello from user space!", 23);
    lseek(fd, 11, SEEK_SET);
    read(fd, buffer, 11);

    post(1,buffer);

    // Test 2
    // expected: PPPPPPPPPPPPPPPPPPPP
    write(fd, "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", 60);
    lseek(fd, 23, SEEK_SET);
    read(fd, buffer, 20);

    post(2,buffer);

    // Test 3
    // expected: GP9TIK33ZJ
    lseek(fd,0,SEEK_SET);
    write(fd,"5PN31WLWKNQYL2LMKjhn17o1TYPJM4pSJagyTA5TkPdIkt49z2skDztgTTSrhbGP9TIK33ZJO6aajDK",79);
    lseek(fd,62,SEEK_SET);
    read(fd, buffer, 10);

    post(3,buffer);

    // Test 4
    // expected: 0123456789abcdef
    write(fd,"0123456789abcdef",16);
    lseek(fd,-16,SEEK_CUR);
    read(fd, buffer, 16);

    post(4, buffer);

    // Test 5
    // expected: PdIkt49z2skDztgTTSrhbGP9TIK33Z
    lseek(fd,40,SEEK_SET);
    lseek(fd,1,SEEK_CUR);
    read(fd, buffer, 30);

    post(5, buffer);

    close(fd);

    return 0;
}