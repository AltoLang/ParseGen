CC = g++

CFLAGS := -Wall -Wextra -Werror -I src -g -std=c++17
LDFLAGS := -lstdc++ -g

SRCDIR := src
OBJDIR := lib
BUILDDIR = bin

rwildcard=$(foreach d,$(wildcard $(1:=/*)),$(call rwildcard,$d,$2) $(filter $(subst *,%,$2),$d))
SRC = $(call rwildcard,$(SRCDIR),*.cpp)
OBJS = $(patsubst $(SRCDIR)/%.cpp, $(OBJDIR)/%.o, $(SRC))

all: $(OBJS) link

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	mkdir -p $(@D)
	$(CC) $(CFLAGS) -c $^ -o $@

link:
	$(CC) -o $(BUILDDIR)/parser.out $(LDFLAGS) $(OBJS)

setup:
	@mkdir $(BUILDDIR)
	@mkdir $(OBJDIR)
	@mkdir $(SRCDIR)