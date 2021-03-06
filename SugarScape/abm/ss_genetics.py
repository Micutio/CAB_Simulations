"""
Genetics Module of the CAB Sugarscape simulation.
Encapsulates all aspects of the agent genetics.
Credit to David Grotzky.
"""

__author__ = 'Michael Wagner'
__version__ = '1.0'

from cab.util.rng import get_RNG


# TODO: Implement proper immune system.
class Chromosome:
    """
    This class handles all biological aspects of an agent.
    """
    def __init__(self, dna):
        """
        Standard initializer.
        :return:
        """
        self.genomes = dna[0:2]
        self.culture = dna[2]
        self.immune_system = dna[3]
        my_generation = max(dna[4][0], dna[4][1]) + 1
        self.generation = (dna[4][0], dna[4][1], my_generation)
        self.meta_sugar = None
        self.meta_spice = None
        self.init_sugar = None
        self.init_spice = None
        self.vision = None
        self.gender = None
        self.fertility = None
        self.dying_age = None
        self.dna_color = None
        # Read dictionary entries as:
        # ----> {attribute: (start index, end index)}
        # TODO: Shift this map into GlobalConstants and automatically generate genome lengths from the given constants.
        self.att_map = {'meta_sugar': (0, 3),
                        'meta_spice': (3, 6),
                        'init_sugar': (6, 12),
                        'init_spice': (12, 18),
                        'vision': (18, 21),
                        'gender': (21, 22),
                        'fertility_1': (22, 28),
                        'fertility_2': (28, 34),
                        'dying_age': (34, 41)}

        self.map_genome_to_attributes()

    def map_genome_to_attributes(self):
        """
        Decodes the genome and creates the attribute of the individual.
        """
        # The meta and init attributes cannot become smaller than 1,
        # even though that is possible by the encoding. We have to avoid that.
        meta_sugar = Chromosome.choose_dominant_gene(self.get_genome_substring('meta_sugar'))
        meta_spice = Chromosome.choose_dominant_gene(self.get_genome_substring('meta_spice'))
        init_sugar = Chromosome.choose_dominant_gene(self.get_genome_substring('init_sugar'))
        init_spice = Chromosome.choose_dominant_gene(self.get_genome_substring('init_spice'))
        vision = Chromosome.choose_dominant_gene(self.get_genome_substring('vision'))
        gender = get_RNG().choice(self.get_genome_substring('gender'))
        f1 = Chromosome.choose_dominant_gene(self.get_genome_substring('fertility_1'))
        f2 = Chromosome.choose_dominant_gene(self.get_genome_substring('fertility_2'))
        dying_age = Chromosome.choose_dominant_gene(self.get_genome_substring('dying_age'))

        self.meta_sugar = max(int(meta_sugar, 2), 1)
        self.meta_spice = max(int(meta_spice, 2), 1)
        self.init_sugar = max(int(init_sugar, 2), 1)
        self.init_spice = max(int(init_spice, 2), 1)
        self.vision = int(vision, 2)
        self.gender = int(gender, 2)
        self.dying_age = int(dying_age, 2)
        self.fertility = (int(f1, 2), int(f2, 2))

        dna = "".join((meta_sugar, meta_spice, init_sugar, init_spice, vision, gender, f1, f2, dying_age))
        self.dna_color = Chromosome.convert_to_color(dna)

    def get_genome_substring(self, key):
        """
        Retrieves the partitions of both genes.
        :param key: The key of the partition entries' location in the dictionary
        :return: Two sub-strings of the genomes
        """
        indices = self.att_map[key]
        start = indices[0]
        end = indices[1]
        return self.genomes[0][start: end], self.genomes[1][start: end]

    @staticmethod
    def choose_dominant_gene(strings):
        """
        Takes two gene strings and returns the dominant one,
        or random if both are dominant/ recessive
        :param strings: Two sub-genes of the chromosome
        :return: The more dominant/ luckier string of both.
        """
        # How do we determine dominance?
        # For now just by looking whether there is an even number of 'ones' in it.
        dominant0 = strings[0].count('1') % 2 == 0
        dominant1 = strings[1].count('1') % 2 == 0
        if (dominant0 and dominant1) or (not (dominant0 or dominant1)):
            return get_RNG().choice([strings[0], strings[1]])
        elif dominant1:
            return strings[0]
        else:
            return strings[1]

    def merge_with(self, mate_chromosome):
        """
        Takes the chromosome from the mate, performs
        all necessary crossovers and returns the resulting DNA
        :param mate_chromosome:
        :return: The child's chromosome.
        """
        # Concept: divide genome in partitions of varying length.
        # Exchange those parts between mother and father gametes?
        genome1 = Chromosome.create_gamete(self.genomes)
        genome2 = Chromosome.create_gamete(mate_chromosome.genomes)
        culture = Chromosome.create_gamete((self.culture, mate_chromosome.culture))
        immune_sys = Chromosome.create_gamete((self.immune_system, mate_chromosome.immune_system))
        # Create a string out of the gene strings
        genome1 = "".join(map(str, genome1))
        genome2 = "".join(map(str, genome2))
        # Order the generation tuple for better overview: (mom, dad)
        if self.gender == 1:
            generation = (self.generation[2], mate_chromosome.generation[2])
        else:
            generation = (mate_chromosome.generation[2], self.generation[2])
        return [genome1, genome2, culture, immune_sys, generation]

    @staticmethod
    def create_gamete(genomes):
        """
        Creates and returns a gamete that consists of parts of
        both genomes in this chromosome.
        :return: Gamete in form of a single bitstring.
        """
        # 1) Generate a random number (gaussian distributed) of
        # random indices which are then used to split the genes at the respective points.
        genome_size = len(genomes[0])
        num_partitions = int(get_RNG().triangular(0, genome_size / 2, genome_size))
        partitions = get_RNG().sample(range(genome_size), num_partitions)
        partitions.sort()  # Now we have all our indices, and sorted.
        partitions.append(genome_size)  # Append the end of the string
        start = 0
        gamete = []
        for p in partitions:
            i = get_RNG().choice([0, 1])
            gamete.extend(genomes[i][start:p])
            start = p
        # 'gamete' is now a list of integers. Convert the ints to strings and join 'em all together.
        return gamete

    def mutate(self):
        """
        Has a chance of 0.5% to perform a random mutation in the dna,
        and a chance of 1% to flip a few bits in the cultural dna.
        :return:
        """
        # Flip bit in genome
        if get_RNG().random() < 0.005:
            length = len(self.genomes)
            index = get_RNG().randrange(length)
            l = list(self.genomes[0])
            l[index] = Chromosome.invert_bit(l[index])
            g1 = "".join(l)

            index = get_RNG().randrange(length)
            l = list(self.genomes[1])
            l[index] = Chromosome.invert_bit(l[index])
            g2 = "".join(l)
            self.genomes = (g1, g2)

        # Flip a bit in culture
        if get_RNG().random() < 0.01:
            length = len(self.culture)
            num_bits_changed = int(get_RNG().triangular(0, 1, length))
            index = get_RNG().sample(range(length), num_bits_changed)
            for i in index:
                self.culture[i] = 1 - self.culture[i]

    @staticmethod
    def invert_bit(bit):
        """
        Takes the bit as a string and inverts it.
        :param bit:
        :return: Inverted bit
        """
        if bit == "0":
            return "1"
        else:
            return "0"

    # This method makes sense only for Lamarckian Evolution!
    # def map_attributes_to_genome(self, attributes):
    #    return

    @staticmethod
    def convert_to_color(dna):
        # l = len(dna)
        # l1 = int(l / 3)
        # l2 = 2 * l1
        r_string = dna[0::3]  # dna[0:l1]
        g_string = dna[1::3]  # dna[l1:l2]
        b_string = dna[2::3]  # dna[l2:]
        r_num = int(r_string, 2)
        g_num = int(g_string, 2)
        b_num = int(b_string, 2)
        r = int((r_num / (2 ** len(r_string))) * 25) * 10
        g = int((g_num / (2 ** len(g_string))) * 25) * 10
        b = int((b_num / (2 ** len(b_string))) * 25) * 10
        return r, g, b
