# This is a package.

# Patch event not to require dates upon creation.
from Products.ATContentTypes.content.event import ATEventSchema

ATEventSchema['startDate'].required = False
ATEventSchema['endDate'].required = False

# Patch content leadImage to add cropscale
from collective.contentleadimage import extender
extender.LeadImageExtender.fields[0].crop_scales = ['mini']
