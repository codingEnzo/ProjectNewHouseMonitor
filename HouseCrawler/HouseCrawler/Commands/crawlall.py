# coding=utf-8

from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")
        parser.add_option("--urlqueue", dest="urlqueue", metavar="SETTING",
                            help="set a url queue name")

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
            if opts.urlqueue:
                self.settings.set('Redis_key', opts.urlqueue, priority='cmdline')
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)

    def run(self, args, opts):
        spidername_base = args[0]
        for cur_num in range(int(args[1])):
            self.crawler_process.crawl(spidername_base, **opts.spargs)
        self.crawler_process.start()
