CC = g++
CFLAGS  = -g -Wall -c
SRCS = Demo.cpp Defects.cpp
OBJS = $(SRCS:.c=.o)

demo: $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o demo

Defects.o: Defects.cpp Defects.hpp
	$(CC) $(CFLAGS) Defects.cpp

Demo.o: Demo.cpp Defects.hpp
	$(CC) $(CFLAGS) Demo.cpp

clean:
	$(RM) demo *.o *~
