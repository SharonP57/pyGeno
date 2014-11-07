import types

import configuration as conf

from tools import UsefulFunctions as uf

class Sequence_modifiers(object) :
	def __init__(self, sources = {}) :
		self.SNPSources = sources

	def addSource(self, name, snp) :
		"Optional, you can keep a dict that records the polynorphims that were mixed together to make self. They are stored into self.SNPSources"
		self.SNPSources[name] = snp

class SequenceSNP(Sequence_modifiers) :
	def __init__(self, alleles, sources = {}) :
		Sequence_modifiers.__init__(self, sources)
		if type(alleles) is types.ListType :
			self.alleles = uf.encodePolymorphicNucleotide(''.join(alleles))
		else :
			self.alleles = uf.encodePolymorphicNucleotide(alleles)
	
class SequenceInsert(Sequence_modifiers) :
	def __init__(self, bases, sources = {}) :
		Sequence_modifiers.__init__(self, sources)
		self.bases = bases

class SequenceDel(Sequence_modifiers) :
	def __init__(self, length, sources = {}) :
		Sequence_modifiers.__init__(self, sources)
		self.length = length

class SNPFilter(object) :
	
	def __init__(self) :
		pass

	def filter(self, chromosome, **kwargs) :
		raise NotImplemented("Must be implemented in child")

class DefaultSNPFilter(SNPFilter) :
	"""Default filtering object, does not filter anything. Doesn't apply indels.
	This is also a template that you can use for own filters. A prototype for a custom filter might be::
		class MyFilter(SNPFilter) :
	
			def filter(chromosome, SNP_Set1, SNP_Set2) :
				if SNP_Set1.alt == SNP_Set2.alt :
					return SequenceSNP(SNP_Set1.alt)

	Where SNP_Set1 and SNP_Set2 are the actual names of the snp sets supplied to the genome. In the context of the function
	they represent single polymorphisms derived from thoses sets that occur at the same position.

	Whatever goes on into the function is absolutely up to you, but in the end, it must return an object of one of the following classes:

		* SequenceSNP

		* SequenceInsert

		* SequenceDel

		* a None value

		"""

	def __init__(self) :
		SNPFilter.__init__(self)

	def filter(self, chromosome, **kwargs) :
	
		warn = 'Warning: the default snp filter ignores indels. IGNORED %s of SNP set: %s at pos: %s of chromosome: %s'
		
		alleles = []
		for snpSet, snp in kwargs.iteritems() :
			pos = snp.start
			if snp.alt[0] == '-' :
				print warn % ('DELETION', snpSet, snp.pos, snp.chromosomeNumber)
			if snp.ref[0] == '-' :
				print warn % ('INSERTION', snpSet, snp.pos, snp.chromosomeNumber)
			else :
				sources[snpSet] = snp
				alleles.append(snp.alt) #if not an indel append the polymorphism
			
		#appends the refence allele to the lot
		refAllele = chromosome.refSequence[pos]
		alleles.append(refAllele)
		sources['ref'] = refAllele

		#optional we keep a record of the polymorphisms that were used during the process
		return SequenceSNP(alleles, sources = sources)