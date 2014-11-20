import unittest
from mock import Mock

import utils

class UtilsColorTests(unittest.TestCase):
    def not_a_test_just_visual_stuff(self):
        # Just in case someone wants a more visual sample.
        # Copy the output to an HTMl file.
        color1 = utils.colors.PURPLE
        color2 = utils.colors.ORANGE

        for i in range(0, 101):
            ratio = i / 100.0
            print '<div style="background: #%s">%s</div>' % (utils.colors.mix_colors(color1, color2, ratio), ratio)

    def test_mix_colors(self):
        # When ratio is zero, we get the first color
        self.assertEqual(
            utils.colors.mix_colors(utils.colors.RED, utils.colors.GREEN, 0),
            utils.colors.RED
        )

        # The more the ratio comes close to one, the more we get of the second
        # color and the less of the first one
        self.assertEqual(
            utils.colors.mix_colors(utils.colors.RED, utils.colors.GREEN, 0.2),
            'cc1900'
        )

        self.assertEqual(
            utils.colors.mix_colors(utils.colors.RED, utils.colors.GREEN, 0.4),
            '993300'
        )

        # When ratio is one, we get the second color
        self.assertEqual(
            utils.colors.mix_colors(utils.colors.RED, utils.colors.GREEN, 1),
            utils.colors.GREEN
        )

        # It can be used to get octarine too, but I'm not sure it's supposed
        # to look like this.
        self.assertEqual(
            utils.colors.mix_colors(utils.colors.PURPLE, utils.colors.ORANGE, 0.5),
            'bf5240'
        )

        # Ratios above the limits do not have effect.
        self.assertEqual(
            utils.colors.mix_colors(utils.colors.RED, utils.colors.GREEN, -15),
            utils.colors.RED
        )
        self.assertEqual(
            utils.colors.mix_colors(utils.colors.RED, utils.colors.GREEN, 3.14),
            utils.colors.GREEN
        )