import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.integrate as integrate
import scipy.special as special
from scipy.optimize import curve_fit
sns.set()


## Create Waveform Function ##
def Efield(t, E0 = 1, w=2*np.pi*0.8, s = 0.4 , phi = 0 ):
    return E0*np.sin(w*t+phi)*np.exp(-0.5*(t)**2/s**2) # sin*gaussian


## Create FFT Function ##
def fourier(t, func):
    freq = np.arange(-1/(abs(t[0])-abs(t[1]))/2, 1/(abs(t[0])-abs(t[1]))/2 , 1/(t[-1]-t[0]))
    ft = np.fft.fft(func)
    ftshift = np.fft.fftshift(ft)
    return np.array([freq, ft, ftshift])


## Create a function that changes the phase of a waveform ##
def change_phase(t,V,phase=0):

    """The change_phase function changes the phase of the input waveform.

       ***PARAMETERS***

       t: Time domain.
       V: Input waveform.
       phase: Desired phase.

       """

    ft = fourier(t , V)
    amp = np.abs(ft[1])
    phi = np.zeros(len(ft[0]))  # make array filled with zeros

    if phase == 0: # avoids redundant calculation
        pass

    else:
        for i in range(-1001,1001):      # fill array with values
            if i >= 0:
                phi[i] = -phase
            if i < 0:
                phi[i] = phase

    pulse = np.fft.ifft(amp*np.exp(1j*phi)) # invFFT signal with new phase
    signal = []  # make empty list

    for i in range(1001,2002):  # invFFT gives signal shifted, but inFFTshift won't work; this is a manual shift
        signal.append(pulse[i])

    for i in range(0,1001):
        signal.append(pulse[i])

    signal = np.asarray(signal)/max(abs(pulse)) # this defines signal for the whole notebook (and normalizes it)

    return signal


## Generate current class ##
class current():

    """The current class is used to simulate different theoretical/toy I-V models. To use: Call current and
       define the desired model as True. Whenever you want to use the model, call the calculate function and
       feed in the desired V. To get an I-V, set V equal to any linspace array of desired size. To get I(t),
       set V equal to your signal, or V(t). Each model has different parameters and should be reviewed accordingly.
       All current types share the same parameters except Simmons. The standard numerical values are set as a
       default in that case."""

    # Initialize current types and variables #

    def __init__(self, height1=1, squeeze1=1, pos1=0, height2=1, squeeze2=1, pos2=0, shift=0,
                 phi_t=8.01088e-19, phi_s=8.01088e-19, z = 0.5e-9, A=1e-9,
                 erf=False, ohm=False, cubic=False, exp=False, double_erf=False, step=False, Simmons=False):

        self.height1 = height1
        self.squeeze1 = squeeze1
        self.pos1 = pos1
        self.height2 = height2
        self.squeeze2 = squeeze2
        self.pos2 = pos2
        self.shift = shift
        self.phi_t = phi_t
        self.phi_s = phi_s
        self.z = z
        self.A = A

        self.erf = erf
        self.ohm = ohm
        self.cubic = cubic
        self.exp = exp
        self.double_erf = double_erf
        self.step = step
        self.Simmons = Simmons

    # Call calculate to generate I[V(t)] #

    def calculate(self, V):

        if self.erf == True:
            calculate = self.height1*special.erf((V-self.pos1)*self.squeeze1) + self.shift
        if self.double_erf == True:
            calculate = self.height1*special.erf((V-self.pos1)*self.squeeze1) + self.height2*special.erf((V - self.pos2)*self.squeeze2) + self.shift
        if self.cubic == True:
            calculate = self.height1*(V*self.squeeze1 - self.pos1)**3 + self.height2*(V*self.squeeze2 - self.pos2) + self.shift
        if self.step == True:
            calculate = self.height1 * (V > self.pos1)
        if self.ohm == True:
            calculate = (V - self.pos1)/self.height1 + self.shift
        if self.exp == True:
            calculate = self.height1*np.exp(-(V*self.squeeze1 - self.pos1)) + self.shift
        if self.Simmons == True:

            I = []

            for i in range(0,len(V)):

                if np.real(V[i])*1.60217662e-19 > -self.phi_t and np.real(V[i])*1.60217662e-19 < self.phi_s:
                    phi_bar = (self.phi_t+self.phi_s-abs(V[i])*1.60217662e-19)/2
                    delta = self.z

                if np.real(V[i])*1.60217662e-19 >= self.phi_s:
                    phi_bar = self.phi_t/2
                    delta = self.z*self.phi_t/(self.phi_t-self.phi_s+abs(V[i])*1.60217662e-19)
                    beta = 23/24

                if np.real(V[i])*1.60217662e-19 <= -self.phi_t:
                    phi_bar = self.phi_s/2
                    delta = self.z*self.phi_s/(self.phi_s-self.phi_t+abs(V[i])*1.60217662e-19)
                    beta = 23/24

                if np.real(V[i])*1.60217662e-19 >= 0 and np.real(V[i])*1.60217662e-19 < self.phi_s:
                    beta = 1-1/24*((abs(V[i])*1.60217662e-19-self.phi_s+self.phi_t)/(abs(V[i])*1.60217662e-19-self.phi_s-self.phi_t))**2

                if np.real(V[i])*1.60217662e-19 > -self.phi_t and np.real(V[i])*1.60217662e-19 < 0:
                    beta = 1-1/24*((abs(V[i])*1.60217662e-19+self.phi_s-self.phi_t)/(abs(V[i])*1.60217662e-19-self.phi_s-self.phi_t))**2

                if np.real(V[i]) >= 0:
                    I.append(1.60217662e-19*self.A/(1.0545718e-34*(2*np.pi*beta*delta)**2)*(
                        phi_bar*np.exp(-2*beta*delta*np.sqrt(9.10938356e-31*2*phi_bar)/1.0545718e-34)
                        -(phi_bar+abs(V[i])*1.60217662e-19)*np.exp(-2*beta*delta*np.sqrt(9.10938356e-31*2)
                                                           *np.sqrt(phi_bar+abs(V[i])*1.60217662e-19)/1.0545718e-34)))

                if np.real(V[i]) < 0:
                    I.append(-1.60217662e-19*self.A/(1.0545718e-34*(2*np.pi*beta*delta)**2)*(
                        phi_bar*np.exp(-2*beta*delta*np.sqrt(9.10938356e-31*2*phi_bar)/1.0545718e-34)
                        -(phi_bar+abs(V[i])*1.60217662e-19)*np.exp(-2*beta*delta*np.sqrt(9.10938356e-31*2)
                                                           *np.sqrt(phi_bar+abs(V[i])*1.60217662e-19)/1.0545718e-34)))

            calculate = np.asarray(I)

        else:
            pass

        return calculate


## Create Phase Sweep  Function ##
def phase_sweep(phi_range, sweep_pts, freq, fft, current, t):

    """This function generates a set of waveforms with different phases. """

    phi_0 = -phi_range/2
    amp = np.abs(fft)
    phase = []
    I = []
    I_integral = []
    sig_array = []
    sig_integral = []


    for i in range(0,sweep_pts): # *****Check to see if this will mess up length stuff

        phi = np.zeros(len(freq))       # re-initialize phi matrix

        for j in range(0, len(freq)):      # fill array with values
            if j >= int(len(freq)/2):
                phi[j] = phi_0
            else:
                phi[j] = -phi_0

        pulse = np.fft.ifft(amp*np.exp(1j*phi)) # get pulse back with new phase
        signal = []

        for k in range(int(len(freq)/2),int(len(freq))):  # manually shift ifft
            signal.append(pulse[k])

        for l in range(int(len(freq)/2)):
            signal.append(pulse[l])

        phase.append(phi_0)             # store phase values
        signal = np.asarray(signal)
        I_integral.append(integrate.simps(x=t, y=current.calculate(signal))) # compute I(t) integral
        I.append(current.calculate(signal))
        sig_array.append(signal)
        sig_integral.append(integrate.simps(x=t, y=signal))
        phi_0 += phi_range/sweep_pts     # compute new phi for next loop
        #plt.plot(t, signal)            # Plot envelope of signals

    phase = np.asarray(phase)
    I_integral = np.asarray(I_integral)
    I = np.asarray(I)
    sig_array = np.asarray(sig_array)

    return [phase, I_integral, sig_array, I, sig_integral]


## Generate Q(V) Data ##
def Q_data1(t, I, V, E0):

    """The Q_data1 function generates data that can be fed into rectify1 function.

       The Q_data1 function simulates rectified charge as a function of driving amplitudes.
       Use this function to compare theoretical values.

       ***PARAMETERS***

       t: Time domain.
       I: Current type. Must be an activated class.
       V: Waveform.
       E0: List of driving amplitudes. Must go from 0 to E0max (i.e. [0,E0]).
       """

    sweep = []

    for i in range(0,len(E0)):
        sweep.append(integrate.simps(x=t, y=I.calculate(V=E0[i]*V))) # probe positive portion of I-V

    sweep = np.asarray(sweep)

    return sweep

def Q_data2(t, I, V, E0):

    """The Q_data function simulates rectified charge as a function of driving amplitudes
       for the V(phi=0) and V(phi=pi) cases. Use this function to compare to theoretical
       values.

       ***PARAMETERS***

       t: Time domain.
       I: Current type. Must be an activated class.
       V: Waveform.
       E0: List of driving amplitudes. Must go from 0 to E0max (i.e. [0,E0]).
       """

    pos_sweep = []
    neg_sweep = []

    for i in range(0,len(E0)):
        pos_sweep.append(integrate.simps(x=t, y=I.calculate(V=E0[i]*V))) # probe positive portion of I-V
        neg_sweep.append(integrate.simps(x=t, y=I.calculate(V=-E0[i]*V))) # probe negative portion

    pos_sweep = np.asarray(pos_sweep)
    neg_sweep = np.asarray(neg_sweep)

    return np.asarray([pos_sweep, neg_sweep])


## Generate Q[V(phi)] map ##
def amplitude_sweep(t, current, amp_pts, maxE0, phi_range, phase_pts, minE0=0, Simmons=False):

    """The amplitude_sweep function takes in a theoretical I-V and produces a rectified charge map by
       sweeping driving amplitude (waveform maximums) and phase. NOTE: Due to the if/and statements
       in the Simmons I-V a separate operation must be done to calculate this case. If the current type
       is the Simmons model, define Simmons=True.

       ***PARAMETERS***

       t: Waveform time domain.
       current: Chosen I-V type from current class.
       amp_pts: Defines number of points in amplitude sweep.
       maxE0: Max waveform amplitude in amplitude sweep.
       phi_range: Phase sweep range.
       phase_pts: Number of points in phase sweep.
       min_E0: Min waveform amplitude in amplitude sweep.
       Simmmons: Toggle Simmons model calculation.

       """

    E0 = np.linspace(minE0,maxE0,amp_pts) # create array of sweep parameters
    I_integral = []  # make empty list
    ft = fourier(t, func = Efield(t,w = 2*np.pi*0.8, s = 0.4, E0=1)) # FFT
    sweep = phase_sweep(phi_range = phi_range, sweep_pts = phase_pts , freq = ft[0], fft = ft[1], current = current , t = t) # Sweep phase and create signal

    if Simmons == True:                  # Due to piecewise nature of Simmons I-V, an additional loop over each point is required

        for i in range(0,amp_pts):
            volt_sweep = []
            for j in range(0,len(sweep[2])):
                volt_sweep.append(integrate.simps(x=t, y = current.calculate(V=E0[i]*sweep[2][j]))) # calculate the integral and store it into the empty list

            I_integral.append(volt_sweep)
        I_integral = np.asarray(I_integral) #turn list into numpy array

    else:

        for i in range(0,amp_pts):
            I_integral.append(integrate.simps(x=t, y = current.calculate(V=E0[i]*sweep[2]))) # calculate the integral and store it into the empty list

        I_integral = np.asarray(I_integral) #turn list into numpy array

    return [sweep, E0, I_integral]


## Function that creates nth order polynomial for fit ##
def arb_poly(x, *params):
    return sum([p*(x**(i+2)) for i, p in enumerate(params)])

def arb_odd_poly(x, *params):
    return sum([p*(x**(2*i+3)) for i, p in enumerate(params)])

def arb_even_poly(x, *params):
    return sum([p*(x**(2*i+2)) for i, p in enumerate(params)])


def rectify1(V, E0, t, Q, fit_terms):

    """The rectify1 function fits the entirety of rectified charge data with minimal adjustment
       to the input data. This function is much more data friendly and less computationally
       expensive.

       The rectify1 function takes in experimental values for the input waveform, amplitudes
       (waveform maximums/minimums), and the result from the Q[V] sweep. It fits a polynomial
       of order 2 and above to any data and reconstructs an I-V curve.

       ***PARAMETERS***

       V: Waveform.
       E0: Waveform maximums from sweep.
       t: Waveform time domain.
       Q: Rectified charge data.

       """

    a_n = []
    rec_current = []
    I_t = []

    popt, pcov = curve_fit(f = arb_poly, xdata=E0 ,   # fit the data
                       ydata = np.real(Q), p0=[1]*(fit_terms)) # default initial guess to be 1

    for i in range(0,len(popt)):
        a_n.append(popt[i]/integrate.simps(V**(i+2),x=t))

    a_n = np.asarray(a_n)

    for i in range(0,len(a_n)):
        rec_current.append(a_n[i]*E0**(i+2))  # reconstruct current
        I_t.append(a_n[i]*V**(i+2))

    rec_I = np.sum(rec_current, axis = 0)
    I_t = np.sum(I_t, axis = 0)

    return np.array([rec_I, I_t, a_n])


def rectify2(V, pos_E0, neg_E0, t, Q_pos, Q_neg, fit_terms):

    """rectify2 fits the even and odd ordered terms of the polynomial. Some complications with
       this method are due to the symmetry of the experimental values about V=0. It is also more
       computationally expensive. When using rectify2, E0 and rectified charge data must be
       separated by its positive and negative parts.

       The rectify2 function takes in experimental values for the input waveform, amplitudes
       (waveform maximums and minimums from positive and negative sweeps respectively), and the
       results from the Q[V(phi=0)] and Q[V(phi=pi)] sweeps. It fits a polynomial of order 2
       and above to any data and reconstructs an I-V curve.

       ***PARAMETERS***

       V: Waveform.
       pos_E0: Waveform maximums from sweep using V(phi=0).
       neg_E0: Waveform minimums from sweep using V(phi=pi).
       t: Waveform time domain.
       Q_pos: Q[V(phi=0)] sweep data. Positive cosine wave as a function of waveform maximums.
       Q_neg: Q[V(phi=pi)] sweep data. Negative cosine wave as a function of waveform maximums.

       """

    a_n = []
    rec_current = []
    I_t = []

    even_order = (Q_pos+Q_neg)/2
    odd_order = (Q_pos-Q_neg)/2

    popt1, pcov1 = curve_fit(f = arb_even_poly, xdata=pos_E0 ,   # fit the even ordered data
                       ydata = np.real(even_order), p0=[1]*(fit_terms)) # default initial guess to be 1


    popt2, pcov2 = curve_fit(f = arb_odd_poly, xdata=pos_E0 ,   # fit the odd ordered data
                       ydata = np.real(odd_order), p0=[1]*(fit_terms))  # default initial guess to be 1


    for i in range(0,len(popt1)):
        a_n.append(popt1[i]/integrate.simps(V**(2*i+2),x=t))
        a_n.append(popt2[i]/integrate.simps(V**(2*i+3),x=t))

    a_n = np.asarray(a_n)
    E0 = np.concatenate((neg_E0,pos_E0), axis=0)

    for i in range(0,len(a_n)):
        rec_current.append(a_n[i]*E0**(i+2))  # reconstruct current
        I_t.append(a_n[i]*V**(i+2))

    rec_I = np.sum(rec_current, axis = 0)
    I_t = np.sum(I_t, axis = 0)

    return np.array([rec_I, I_t, a_n])


## Sweep I(t), dI/dt, and FFT of dI/dt ##
def current_sweep(V, E0, t, a_n, current_model, theory = False, rectified = False):

    """This function creates a 3D map of I(t), dI/dt, and the emitted field FFT
        as a function of driving voltage amplitude (waveform maximums). You can feed in either a theoretical I-V
        or an I-V that has been rectified in a previous section.

        ***PARAMETERS***

        V: Waveform.
        E0: Array of waveform amplitudes.
        t: Time axis.
        a_n: Fitting coefficients
        theory: Toggle if feeding in theoretical model.
        rectified: Toggle if feeding in rectified I-V.

        """

    if theory == True and rectified == True or theory == False and rectified == False:

        return print('Error: Select current type')

    elif rectified == True:

        I_map = np.zeros((len(V),len(E0)))
        Idt_map = np.zeros((len(V), len(E0)-1))
        IFT_map = np.zeros((len(V), len(E0)-1))

        for j in range(0,len(E0)):

            I_t = []

            for i in range(0,len(a_n)):
                I_t.append(a_n[i]*V**(i+2)*E0[j])

            I_t = np.sum(I_t, axis = 0)
            I_dt = np.diff(I_t)/np.diff(t)
            IFT = fourier(t, I_dt)

            I_map[j,:] = I_t
            Idt_map[j,:] = I_dt
            IFT_map[j,:] = np.abs(IFT[2])


    elif theory == True:

        I_map = []
        Idt_map = []
        IFT_map = []


        for i in range(0, len(E0)):
            I_map.append(current_model.calculate(E0[i]*V))
            Idt_map.append(np.diff(current_model.calculate(E0[i]*V))/np.diff(t))
            IFT = fourier(t, np.diff(current_model.calculate(E0[i]*V))/np.diff(t))
            IFT_map.append(np.abs(IFT[2]))

        I_map = np.asarray(I_map)
        Idt_map = np.asarray(Idt_map)
        IFT_map = np.asarray(IFT_map)

    return [I_map, Idt_map, IFT[0], IFT_map]
