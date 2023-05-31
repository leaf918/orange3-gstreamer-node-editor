pth_plugin = 'txt_playbin.txt'
blocks = []
cur_info_block = []
for line in open(pth_plugin, 'r'):
    if len(line) == 1 and line[0] == '\n':
        blocks.append(cur_info_block)
        cur_info_block = []
        continue
    if line[0] != ' ':
        # new block,as title
        if len(cur_info_block) > 0: blocks.append(cur_info_block)
        cur_info_block = []
        cur_info_block.append(line)  # title,
        continue
    else:
        #
        cur_info_block.append(line)  # title,content
if len(cur_info_block) > 0:
    blocks.append(cur_info_block)
    cur_info_block = []


def refine_block_to_json(b):
    title = None
    pa = []
    for i, c in enumerate(b):
        if i == 0:
            title = c
            continue
        c = c.strip().split('  ')
        pa.append([c[0], c[1]])


def refine_property_to_json(p):
    if not p[0].startswith('Element Properties'):
        return
    title = None
    pa = []
    for i, c in enumerate(p):
        if i == 0:
            title = c
            continue
        if c.startswith('   '):
            # not property name
            continue
        pa.append(c.split(':')[0].strip())
    return pa


jss = [refine_property_to_json(i) for i in blocks]

# print('plugin info blocks %s' % len(blocks))
print('plugin info property %s' % jss)
