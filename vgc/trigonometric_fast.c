/*This module consists of sped-up mathematical functions, using
* Taylor polynomials and/or self-constructed estimations. Since
* Python does not recognize c-floats, all values are returned as
* integers, 10^6 times larger than the actual value. The returned
* values must be divided by 10^6.
*
* Functions:
* int roundToNearest(float x, float multiple)
* int cos_t(float x)
* int sin_t(float x)
* int arctan_t_2(float x)
* int tan_t(float x)
*/
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

const float f_pi = 3.141592653589f;

int roundToNearest(float x, float multiple){
    /*Returns the closest multiple n of multiple to the given
    * x, according to: multiple*n =/closest to/= x.
    * For example, x = 13 and multiple = 5 would return 3,
    * since 5*3 is closest to 13.
    */
    x = x + multiple/2;
    if(x < 0){
        return 0;
    }
    return(int)(x / multiple);
}

int cos_t(float x){
    /*Returns the cosine value of the given x.
    * Works for all values of x. Larger values may be slow.
    * The function works by first finding the closest multiple
    * of pi/6 to the given value x, and then using the Taylor
    * polynome around the given multiple of pi/6.
    */
    float mult = 1000000.0f;
    while(x < 0){
        x += 2*f_pi;
    }
    while(x > 2*f_pi){
        x -= 2*f_pi;
    }
    if(x > f_pi){
        x -= f_pi;
        mult = -1000000.0f;
    }
    int point = roundToNearest(x, f_pi/6);
    float a = x - point*f_pi/6;
    switch(point){
        case 0:
            return(int)(mult*(1 - 0.5*(a * a)));
        case 1:
            return((int)(mult*(0.866f - 0.5f*(a) - 0.433f*(a*a))));
        case 2:
            return((int)(mult*(0.5f - 0.866f*(a) - 0.25f*(a*a))));
        case 3:
            return((int)(mult*(-x + f_pi/2)));
        case 4:
            return((int)(mult*(-0.5f - 0.866f*(a) + 0.25f*(a*a))));
        case 5:
            return((int)(mult*(-0.866f - 0.5f*(a) + 0.433f*(a*a))));
        case 6:
            return((int)(mult*(-1 + 0.5f*(a*a))));
        default:
            return 2;
    }
}

int arctan_t_2(float x){
    /*Returns the arctan value of the given x. If a negative
    * value is needed, make use of the identity 
    * arctan(-x) = -arctan(x).
    * The function used is self-produced, and can therefore not
    * be properly proved. The returned value differs with at most
    * 0.0874 radians.
    */
    int mult = 1000000;
    float a = 0.76f*x;
    float b = 0.2f*x*x;
    float pi_2 = f_pi/2;
    return (int)(mult*(pi_2 - (pi_2/(1 + a + b))));
}

int tan_t(float x){
    /*This tangens only operates between x = 0
    * and x = pi/2, because view_controller only
    * calls for such values of x.
    */
    int mult = 1000000;
    if(x < 0 || x > f_pi/2){
        return 0;
    }
    if(x < 0.48f){
        return (int)(mult*(x + (x*x*x)/3));
    }
    else{
        float a = x - f_pi/2;
        return (int)(mult*(-1/a + 0.333f*a + 0.022f*(a*a*a)));
    }
}

int sin_t(float x){
    /* Given a float x, which should be in radians,
    we return its sine value using the fast version of the cosine.
    For more information, see the function cos_t(float x).
    */
    return cos_t(f_pi/2 - x);
}

int main(){
    return 0;
}

