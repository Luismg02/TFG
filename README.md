# TFG
Este repositorio contiene todos los archivos mencionados en la memoria del TFG

# MÁQUINAS VIRTUALES

Para facilitar la tarea de recreación de bugs tanto a nivel del espacio de usuario como del kernel de Linux, se pueden encontrar las tres máquinas virtuales usadas dentro de la carpeta MaquinasVirtuales. En dicha carpeta, se hallan todos los archivos necesarios para que el usuario interesado pueda usar la máquina virtual para recrear los bugs directamente desde allí. Para llevar a cabo la instalación de la máquina virtual en virtualbox, se pueden seguir los siguientes pasos:
1. Clic sobre Nueva.
2. Rellenamos el campo Nombre y seleccionamos la imagen ISO correspondiente.
3. Pulsamos en Siguiente.
4. Establecemos un nombre de usuario y contraseña.
5. Pulsamos en Siguiente.
6. Asignamos 4096 MB de memoria RAM y 2 CPUs.
7. Pulsamos en Siguiente.
8. Asignamos un tamaño de disco de 25 GB.
9. Pulsamos en Siguiente.
10. Pulsamos en Terminar.

# HERRAMIENTA DE ASAN

Dentro de este repositorio, se puede encontrar la carpeta ASan donde se hallan todos los archivos mencionados en la memoria del TFG que han sido usados para la recreación de bugs en el espacio de usuario. Para llevar a cabo la identificación de bugs por parte de ASan, es necesario seguir los siguientes pasos:
 1. Creación de un archivo .c con el código a compilar (en este caso los archivos se encuentran ya creados en la carpeta ASan).
 2. Ejecutar el comando sudo gcc -fsanitize=address -O1 -g archivo_sin_compilar.c -o archivo_compilado.c
 3. Ejecución del comando ./archivo compilado.

Respecto al uso del primer comando para realizar la compilación, esta es una explicación de cada una de las opciones usadas:
1. sudo: esta palabra clave se utiliza para ejecutar el comando como superusuario o administrador. Esto es necesario si el usuario no tiene permisos suficientes para realizar la operación.
2. gcc: Es el compilador de GNU para el lenguaje de programación C. Se utiliza para traducir el código fuente escrito en C a código de máquina ejecutable. Este es el lenguaje de programación usado en cada uno de los tests.
3. -fsanitize=address: Esta opción habilita el AddressSanitizer (ASan), como ya hemos comentado nos permitirá detectar errores de memoria en tiempo de ejecución. Al compilar con esta opción, el binario resultante incluirá instrumentación para verificar la memoria durante la ejecución.
4. -O1: Esta opción especifica el nivel de optimización. En este caso, se utiliza el nivel 1 de optimización. Esto significa que el compilador aplicará optimizaciones básicas para mejorar el rendimiento del código sin sacrificar la legibilidad.
5. -g: Esta opción incluye información de depuración en el binario generado. La información de depuración permite rastrear errores y depurar el programa más fácilmente.
6. archivo_sin_compilar.c: Es el archivo fuente que se compilará. Debe estar presente en el directorio actual o especificar la ruta completa al archivo.
7.-o archivo_compilado: Esta opción especifica el nombre del archivo de salida. En este caso, el binario resultante se llamará “archivo compilado”.

# HERRAMIENTA DE KASAN

Dentro de este repositorio, se puede encontrar la carpeta KASAN donde se hallan todos los módulos mencionados en la memoria del TFG que han sido insertados en el kernel de Linux para la recreación de bugs en el espacio del kernel. Si el usuario no hace uso de la máquina proporcionada en la carpeta de MaquinasVirtuales (KASAN), deberá de seguir los siguientes pasos para su activación:
1. Descargar el código fuente de Linux: usamos el comando git clone https://github.com/torvalds/linux.git.
2. Instalar las herramientas de desarrollo: usaremos herramientas de desarrollo como gcc,make, libncurses-dev, flex y bison. Para llevar a cabo la instalación hacemos uso del comando sudo apt-get install gcc make libncurses-dev flex bison.
3. Configuración del kernel: Nos debemos situar donde se encuentra el código fuente del kernel de Linux que descargamos en el primer paso. Para abrir la interfaz de configuración debemos de usar el comando make menuconfig. Hemos habilitado las siguientes configuraciones haciendo uso de de la búsqueda /:
    • CONFIG KASAN: dicha opción la habilitamos siguiendo realizando los siguientes pasos: Kernel Hacking -> Memory Debugging -> Lo Activamos pulsando la barra espaciadora -> Accedemos pulsando la tecla Enter -> Activamos pulsando la barra espaciadora la opción Generic. Gracias a esta configuración ya tenemos activado KASAN en modo genérico.
    • CONFIG KASAN OUTLINE: dicha opción la habilitamos siguiendo los siguientes pasos: KASAN -> Instrumentation type. Gracias a esta configuración ya tenemos habilitado el seguimiento de pila para KASAN.
    • CONFIG DEBUG INFO: dicha opción no debe estar habilitada, para comprobarlo debemos de seguir los siguientes pasos: Kernel Hacking -> Compile-time -> Debug Information -> Disable Debug Information. Al no estar marcada dicha opción tenemos habilitada la información de depuración.
4. Compilar el kernel con las nuevas características: Para llevar a cabo todo el proceso de compilación debemos de ejecutar el comando make en la carpeta donde tenemos el código fuente del kernel de linux. A medida que se va compilando el kernel se sufrirá varias interrupciones debido a la necesidad de tener instalados una serie de paquetes. Los paquetes que han sido necesarios instalar para poder realizar el proceso de compilación han sido los siguientes: libssl-dev, libelf-dev, dkms,libudev-dev, libpci-dev, libiberty-dev y autoconf. Habrá que tratar con nuevos errores y seguir los siguientes pasos para llegar a la solución:
    • Tamaño de Stack: Debemos de cambiar el tamaño de stack para que pueda compilar dentro de FRAME WARN. Para ello, establecemos un nuevo tamaño de 2048 bytes cambiando su antiguo valor de 1024 bytes. Dicha opción, la podemos encontrar en la siguiente ruta: Kernel Hacking -> Compile Time -> Warn for stacks frames.
    • Fallo Certificados: fallo en las claves de confianza. Para solventar este error se tiene que comentar las líneas donde apareciera CONFIG_SYSTEM_TRUSTED_KEYS
    dentro del .config.
    • Nuevo Fallo De Certificados: fallo en las claves de revocación. Es necesario comentar las líneas en las que aparezca CONFIG_SYSTEM_REVOCATION_KEYS para solventar el problema.

Para finalizar debemos de seguir los siguientes pasos:
1. Comando make para compilar el kernel dentro de la carpeta de Linux que habíamos clonado.
2. Comando make modules install.
3. Comando make install.

Una vez ejecutado los tres comandos anteriores ya podemos iniciar la máquina virtual con la imagen de arranque que tiene KASAN habilitado. Una vez hecho esto, podemos comprobar que está configurado KASAN ejecutando el siguiente comando: grep CONFIG_KASAN /boot/config-$(uname-r). Si nos aparece CONFIG_KASAN=y significa que está configurado. Los pasos para recrear los respectivos bugs son los siguientes (los pasos 1,2 y 3 no son necesarios ya que se encuentran en la carpeta KASAN):
1. Crear un archivo que pueda ser pasado a la extensión .ko (extensión que hace referencia a un módulo del kernel de Linux), para ello creamos un archivo escrito en el lenguaje de programación C.
2. Creaciónn del archivo Makefile(archivo de texto que describe larelación entre los archivos fuente del programa y los encabezados que se compilarán)que me genera la extensión .ko.
3. Ejecutamos el comando make donde se encuentra el archivo Makefile creado en el paso anterior y se nos generan diversos archivos.
4. Insertamos el módulo con el comando insmod nombre.ko.
5. Ejecución del comando dmesg para visualizar el log de KASAN.

Finalmente, cabe destacar que en la máquina virtual KASAN_INLINE se puede encontrar activada la configuración de KASAN pero con la opción inline en vez de outline como la máquina anterior. Esta configuración hace que el compilador inserte directamente comprobaciones de accesibilidad de memoria antes de cada acceso a la memoria.Es más rápido que KASAN_OUTLINE(da x2 de impulso para algunas cargas de trabajo),pero hace que el tamaño .text del kernel sea mucho mayor.

# WEB SCRAPING

En la carpeta WebScraping se puede encontrar el código python utilizado.

# BASE DE DATOS

En la carpeta BasedeDatos se puede encontrar la base de datos.

# FRONTEND

En la carpeta Frontend está disponible todo el código utilizado en la implementación de dicho frontend a través de la tecnología de Django. Cabe mencionar, los pasos a seguir para hacer funcionar la aplicación web en local:

1. Instalamos Django con el comando pip install Django.
2. Accedemos a la carpeta Django y ejecutamos el comando python manage.py startapp aplicacion.
3. Accedemos al archivo settings.py y nos vamos a la parte de DATABASES y tenemos que cambiar el
campo Name por la ruta directa a la base de datos.
4. Finalmente, ejecutamos el servidor de desarrollo con el comando python manage.py runserver.

Es importante destacar que si se hace alguna modificación será necesario aplicar las migraciones con los dos comandos siguientes: python manage.py makemigrations y python manage.py migrate. Además, si queremos realizar consultas a la base de datos debmos de descargarnos sqlite3 desde su página web, descomprimirlo y mover el archivo sqlite3.exe a la ruta raíz del proyecto.