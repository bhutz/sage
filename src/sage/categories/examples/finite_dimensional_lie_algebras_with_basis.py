r"""
Examples of a finite dimensional Lie algebra with basis
"""
#*****************************************************************************
#  Copyright (C) 2014 Travis Scrimshaw <tscrim at ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.sets.family import Family
from sage.categories.all import LieAlgebras
from sage.modules.free_module import FreeModule
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element_wrapper import ElementWrapper
from sage.categories.examples.lie_algebras import LieAlgebraFromAssociative as BaseExample

class AbelianLieAlgebra(Parent, UniqueRepresentation):
    r"""
    An example of a finite dimensional Lie algebra with basis:
    the abelian Lie algebra.

    This class illustrates a minimal implementation of a finite dimensional
    Lie algebra with basis.
    """
    @staticmethod
    def __classcall_private__(cls, R, names, M=None):
        """
        Normalize input to ensure a unique representation.

        EXAMPLES::

            sage: from sage.categories.examples.finite_dimensional_lie_algebras_with_basis import AbelianLieAlgebra
            sage: A1 = AbelianLieAlgebra(QQ, 'x,y,z')
            sage: A2 = AbelianLieAlgebra(QQ, ['x','y','z'])
            sage: A3 = AbelianLieAlgebra(QQ, ['x','y','z'], FreeModule(QQ, 3))
            sage: A1 is A2 and A2 is A3
            True
        """
        if isinstance(names, str):
            names = names.split(',')
        if M is None:
            M = FreeModule(R, len(names))
        elif len(names) != M.dimension():
            raise ValueError("number of generators is not correct")
        else:
            M = M.change_ring(R)
        return super(AbelianLieAlgebra, cls).__classcall__(cls, R, tuple(names), M)

    def __init__(self, R, names, M):
        """
        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: TestSuite(L).run()
        """
        self._ordered_indices = range(M.dimension())
        self._M = M
        cat = LieAlgebras(R).FiniteDimensional().WithBasis()
        Parent.__init__(self, base=R, names=names, category=cat)

    def _construct_UEA(self):
        """
        Construct the universal enveloping algebra of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L._construct_UEA()
            Multivariate Polynomial Ring in a, b, c over Rational Field
        """
        from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
        return PolynomialRing(self.base_ring(), self.variable_names())

    def _repr_(self):
        """
        EXAMPLES::

            sage: LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            An example of a finite dimensional Lie algebra with basis:
             the abelian Lie algebra with generators ('a', 'b', 'c')
             over Rational Field
        """
        ret = "An example of a finite dimensional Lie algebra with basis:" \
              " the abelian Lie algebra with generators {!r} over {}".format(
                         self.variable_names(), self.base_ring())
        B = self._M.basis_matrix()
        if not B.is_one():
            ret += " with basis matrix:\n{!r}".format(B)
        return ret

    def _element_constructor_(self, x):
        """
        Construct an element of ``self`` from ``x``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L(0)
            (0, 0, 0)
            sage: M = FreeModule(ZZ, 3)
            sage: L(M([1, -2, 2]))
            (1, -2, 2)
        """
        return self.element_class(self, self._M(x))

    @cached_method
    def zero(self):
        """
        Return the zero element.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.zero()
            (0, 0, 0)
        """
        return self.element_class(self, self._M.zero())

    def basis_matrix(self):
        """
        Return the basis matrix of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.basis_matrix()
            [1 0 0]
            [0 1 0]
            [0 0 1]
        """
        return self._M.basis_matrix()

    def subalgebra(self, gens, names='x'):
        """
        Return a subalgebra of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.inject_variables()
            Defining a, b, c
            sage: L.subalgebra([2*a+b, b + c], 'x,y')
            An example of a finite dimensional Lie algebra with basis:
             the abelian Lie algebra with generators ('x', 'y')
             over Rational Field with basis matrix:
            [   1    0 -1/2]
            [   0    1    1]
        """
        if isinstance(names, str):
            names = names.split(',')
        if len(names) == 1 and len(gens) != 1:
            names = tuple( names[0] + str(i) for i in range(len(gens)) )
        N = self._M.subspace([g.value for g in gens])
        return AbelianLieAlgebra(self.base_ring(), names, N)

    def basis(self):
        """
        Return the basis of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.basis()
            Finite family {'a': (1, 0, 0), 'c': (0, 0, 1), 'b': (0, 1, 0)}
        """
        names = self.variable_names()
        d = {names[i]: self.element_class(self, b)
             for i,b in enumerate(self._M.basis())}
        return Family(d)

    lie_algebra_generators = basis

    def gens(self):
        """
        Return the generators of ``self``.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.gens()
            ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        """
        G = self.lie_algebra_generators()
        return tuple(G[i] for i in self.variable_names())

    def free_module(self):
        """
        Return ``self`` as a free module.

        EXAMPLES::

            sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
            sage: L.free_module()
            Vector space of dimension 3 over Rational Field

            sage: L.inject_variables()
            Defining a, b, c
            sage: S = L.subalgebra([2*a+b, b + c], 'x,y')
            sage: S.free_module()
            Vector space of degree 3 and dimension 2 over Rational Field
            Basis matrix:
            [   1    0 -1/2]
            [   0    1    1]
        """
        return self._M

    class Element(BaseExample.Element):
        def _bracket_(self, y):
            """
            Return the Lie bracket ``[self, y]``.

            EXAMPLES::

                sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
                sage: L.inject_variables()
                Defining a, b, c
                sage: a.bracket(c)
                (0, 0, 0)
                sage: a.bracket(b).bracket(c)
                (0, 0, 0)
            """
            return self.parent().zero()

        def lift(self):
            """
            Return the lift of ``self`` to the universal enveloping algebra.

            EXAMPLES::

                sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
                sage: L.inject_variables()
                Defining a, b, c
                sage: elt = 2*a + 2*b + 3*c
                sage: elt.lift()
                2*a + 2*b + 3*c
            """
            UEA = self.parent().universal_enveloping_algebra()
            gens = UEA.gens()
            return UEA.sum(c * gens[i] for i, c in self.value.iteritems())

        def to_vector(self):
            """
            Return ``self`` as a vector.

            EXAMPLES::

                sage: L = LieAlgebras(QQ).FiniteDimensional().WithBasis().example()
                sage: L.inject_variables()
                Defining a, b, c
                sage: elt = 2*a + 2*b + 3*c
                sage: elt.to_vector()
                (2, 2, 3)
            """
            return self.value

Example = AbelianLieAlgebra

