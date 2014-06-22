from six import add_metaclass

from rx import Observable, AnonymousObservable
from rx.observable import ObservableMeta
from rx.internal import ArgumentOutOfRangeException
from rx.internal.utils import adapt_call

@add_metaclass(ObservableMeta)
class ObservableTakeWhile(Observable):
    """Note that we do some magic here by using a meta class to extend 
    Observable with the methods in this class"""

    def take_while(self, predicate):
        """Returns elements from an observable sequence as long as a specified
        condition is true. The element's index is used in the logic of the 
        predicate function.
        
        1 - source.take_while(lambda value: value < 10)
        2 - source.take_while(lambda value, index: value < 10 or index < 10)
        
        Keyword arguments:
        predicate -- A function to test each element for a condition; the 
            second parameter of the function represents the index of the source
            element.

        Returns an observable sequence that contains the elements from the 
        input sequence that occur before the element at which the test no 
        longer passes.        
        """
        predicate = adapt_call(predicate)
        observable = self
        def subscribe(observer):
            running, i = [True], [0]

            def on_next(value):
                if running[0]:
                    try:
                        running[0] = predicate(value, i[0])
                    except Exception as exn:
                        observer.on_error(exn)
                        return
                    else:
                        i[0] += 1
                    
                    if running[0]:
                        observer.on_next(value)
                    else:
                        observer.on_completed()
    
            return observable.subscribe(on_next, observer.on_error, observer.on_completed)
        return AnonymousObservable(subscribe)
        
