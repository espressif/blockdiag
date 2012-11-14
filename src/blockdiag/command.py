# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re
import blockdiag
import blockdiag.builder
import blockdiag.drawer
import blockdiag.parser
from blockdiag.utils.bootstrap import Application, Options

# for compatibility
from blockdiag.utils.bootstrap import create_fontmap, detectfont
create_fontmap
detectfont


class BlockdiagOptions(Options):
    def build_parser(self):
        super(BlockdiagOptions, self).build_parser()
        self.parser.add_option(
            '-s', '--separate', action='store_true',
            help='Separate diagram images for each group (SVG only)'
        )


class BlockdiagApp(Application):
    module = blockdiag

    def parse_options(self):
        self.options = BlockdiagOptions(self.module).parse()

    def build_diagram(self, tree):
        if not self.options.separate:
            return super(BlockdiagApp, self).build_diagram(tree)
        else:
            DiagramBuilder = self.module.builder.SeparateDiagramBuilder
            DiagramDraw = self.module.drawer.DiagramDraw

            basename = re.sub('.svg$', '', self.options.output)
            for i, group in enumerate(DiagramBuilder.build(tree)):
                outfile = '%s_%d.svg' % (basename, i + 1)
                draw = DiagramDraw(self.options.type, group, outfile,
                                   fontmap=self.fontmap,
                                   antialias=self.options.antialias,
                                   nodoctype=self.options.nodoctype,
                                   transparency=self.options.transparency)
                draw.draw()
                draw.save()

            return 0


def main():
    return BlockdiagApp().run()