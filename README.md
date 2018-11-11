# regex-builder
A set of scripts to build a regex from a list of words

#### Background

For nano (terminal-based text-editor), the syntax files are made based on regular expressions (regex(es) from now on), syntax files that I, twice now, for PowerPC GNU assembler syntax and for the original 8086/8088 intel assembly (according to wikipedia), spent significant time creating regexes and *simplifying* them to less characters, in the hope that the interpreter also finds them simpler.

After creating those regexes, which took some work, I noticed that other syntax files were just, in a way, *ignoring-the-advantages-and-usefulness-of-the-regex-engine* regexes, in my opinion of course. Making my effort of creating those *beautiful* regexes feel ignored.

And so I had the need to make another syntax file, this time for *smali*, the Dalvik VM bytecode/assembler, and I did not want to have to make the effort of building those regexes again.

With that came this set of scripts

#### The scripts

These are some *simple* scripts, I believe, making use of character trees to map the *to-be-regexed* words, you simply input a list of words, or a file with a list of words to be regexed and it prints *i hope* a regex to match it.

The `simple_regex_builder.py` just creates the regex by *joining* from the first characters,
something like making *aaa*, *aab* and *acc*, the regex: `a(a[ab]|cc)`, which is a great deal to start with.

In the soon to implement (i hope) `better_regex_builder.py` I'll try to build regexes by checking also the final words
making (hopefully) *aaa*, *aab*, *acc* and *bcc* -> *aa[ab]|[ab]cc*.

#### Usefulness

I believe this is only useful to do what it says it does, it's not some sort of artIFicial intelligence (although it uses, currently, only 29 if's for 259 lines of code).

You can use it for some kind of research, most probably personal, I tried to comment the code, if you're new to programming (*you wouldn't be here in the first place*) I suggest trying to port this script to another language (Java/C# would be nice, C would be nicer), I know myself will port this to C.
