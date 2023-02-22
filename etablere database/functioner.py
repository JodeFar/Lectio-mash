import ahocorasick


def get_navne_liste(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        navne_liste = file.readlines()
        navne_liste = list(map(lambda e: e[:-1], navne_liste))
        return navne_liste




def aho_find_index_shared_names(school_names, list_names):
    automaton = ahocorasick.Automaton()
    for idx, element in enumerate(school_names):
        automaton.add_word(element, idx)
    automaton.make_automaton()

    # Find the common element indices
    common_element_indices = []

    for idx, element in enumerate(list_names):
        matches = [match[1] for match in automaton.iter(element) if school_names[match[1]] == element]
        if matches:
            common_element_indices.append(idx)

    return common_element_indices