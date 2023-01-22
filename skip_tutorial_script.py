# Skip tutorial script by RLN

# Chooses a random look for your character then skips the tutorial.

HEAD_SPRITES = [0,3,5,6,7]
BODY_SPRITES = [1,4]

wait_for_appearance_packet = False

def done(api):
    return not api.in_rect(244, 719, 55, 49)


def go(api):
    global wait_for_appearance_packet

    if not wait_for_appearance_packet:
        wait_for_appearance_packet = True
        api.log("waiting for appearance packet")
        return 2000

    if api.is_appearance_screen():
        head_gender = api.random(0, 1)
        head = HEAD_SPRITES[api.random(0, len(HEAD_SPRITES)-1)]
        body_type = BODY_SPRITES[api.random(0, len(BODY_SPRITES)-1)]
        hair_colour = api.random(0, 9)
        top_colour = api.random(0, 14)
        pants_colour = api.random(0, 14)
        skin_colour = api.random(0, 4)

        api.log("GENDER=%d" % head_gender)
        api.log("HEAD=%d" % head)
        api.log("BODY=%d" % body_type)
        api.log("HAIR=%d" % hair_colour)
        api.log("TOP=%d" % top_colour)
        api.log("PANTS=%d" % pants_colour)
        api.log("SKIN=%d" % skin_colour)

        api.send_appearance_update(head_gender, \
                               head, \
                               body_type, \
                               hair_colour, \
                               top_colour, \
                               pants_colour, \
                               skin_colour)
        api.log("sent appearance")


    api.skip_tutorial()

    return 5000
