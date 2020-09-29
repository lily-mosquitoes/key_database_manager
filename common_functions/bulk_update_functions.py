def _transpose_file_if_needed(file, couplets, species):

    columns = file[0][1:]
    if len(columns) < 1:
        raise Exception('U001', 'file not formatted correctly')

    col_is_couplets = [col in couplets for col in columns]
    col_is_species = [col in species for col in columns]

    if sum(col_is_couplets) > 0:
        if sum(col_is_couplets) == len(columns):
            return list(map(list, zip(*file))) # transposed file

        else:
            not_found = ', '.join([columns.index(n) for n in range(len(columns)) if col_is_couplets[n] == False])
            raise Exception('U003', f'couplet not found: {not_found}')

    elif sum(col_is_species) > 0:
        if sum(col_is_species) == len(columns):
            return file # normal file

        else:
            not_found = ', '.join([columns.index(n) for n in range(len(species)) if col_is_species[n] == False])
            raise Exception('U004', f'species not found: {not_found}')

    else:
        raise Exception('U002', 'no valid couplets or species')

def import_bulk_update_file(path, couplets, species):

    file = open(path, 'rt').read().strip().split('\n')
    if len(file) <= 1:
        raise Exception('U001', 'file not formatted correctly')

    file = [line.split(',') for line in file]

    # file must be line=couplets, cols=species
    file = _transpose_file_if_needed(file, couplets, species)

    species = file.pop(0)[1:]
    couplets = list()
    states = list()
    for l in file:
        cp_name = l.pop(0)
        couplets.append(cp_name)
        states.append(l.copy())
    return couplets, species, states
