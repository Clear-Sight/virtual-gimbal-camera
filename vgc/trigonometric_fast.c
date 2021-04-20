#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <sys/time.h>
//gcc -shared -o libhello.so -fPIC hello.c

const float f_pi = 3.141592653589f;

int closest(float n, float x){
    int n_temp = (int)(n * 100);
    int x_temp = (int)(x * 100);
    if(x_temp > n_temp){
        if(x_temp/2 > n_temp){
            return 0;
        }
        return 1;
    }
    n_temp += x_temp/2;
    n_temp -= (n_temp%x_temp);
    return n_temp/x_temp;
}

bool equals(float x, float y){
    return(fabs(x - y) <= 0.001f);
}

bool close(float x, float y){
    float comp = f_pi/12;
    return((x - y) <= comp && (y - x) <= comp);
}

int roundToNearest(float x, float multiple){
    x = x + multiple/2;
    if(x < 0){
        return 0;
    }
    //int x_temp = (int)(x * 100);
    //int m_temp = (int)(multiple * 100);
    return(int)(x / multiple);
}

int cos_t(float x){
    /*Returns the cosine value, multiplied by 1000000.
    * This is because Python cannot interpret a float.
    * Therefore when the value is fetched it must be 
    * divided by 1000000 (10^6). 
    */
    //printf("Input: as float: %f, as int: %i\n", x);
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
    //int point = closest(x, f_pi/6);
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

    
int arctan_t(float x){
    /**
    Fast version of arctan(x)
    */
    int mult = 1000000;
 
    //int point = roundToNearest(x, f_pi/6);
    //float a = x - point*f_pi/6;
    if(x < 0 || x > f_pi/6){
        return 0;
    }
    else{
        return (int)(mult * (x - (x * x * x) / 3));
 }
}

int arctan_t_2(float x){
    int mult = 1000000;
    float a = 0.8f * x;
    float b = 0.1f * x*x;
    float c = 0.05f * x * x *x;
    float pi_2 = f_pi/2;
    return (int)(mult*(pi_2 - (pi_2 / (1 + a + b + c))));
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


    /*
    if(close(x, 0)){
        return((int)(mult*(1 - 0.5*(x * x))));
    }
    if(close(x, f_pi/6)){
        return((int)(mult*(0.866f - 0.5f*(x - f_pi/6))));
    }
    if(close(x, f_pi/3)){
        return((int)(mult*(0.5f - 0.866f*(x - f_pi/3))));
    }
    if(close(x, f_pi/2)){
        return((int)(mult*(-x + f_pi/2)));
    }
    if(close(x, 2*f_pi/3)){
        return((int)(mult*(-0.5f - 0.866f*(x - 2*f_pi/3))));
    }
    if(close(x, 5*f_pi/6)){
        return((int)(mult*(-0.866f - 0.5f*(x - 5*f_pi/6))));
    }
    if(close(x, f_pi)){
        return((int)(mult*(-1 + 0.5f*(x - f_pi)*(x - f_pi))));
    }*/
    
    //printf("None found, nearest point = %f, 5pi/6 = %f\n", point, 5*pi/6);
    //printf("%i", point == 5*pi/6);

int sin_t(float x){
    return cos_t(f_pi/2 - x);
}

int getInt(){
    return 1337;
}

char getChar(){
    return 'b';
}
void test_time_closest(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000000.0f; i++){
        bool x = closest(1.5f, 0.5f);
    }
    gettimeofday(&stop, NULL);
    printf("Closest took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

void test_time_close(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000000.0f; i++){
        bool x = close(1.5f, 0.5f);
    }
    gettimeofday(&stop, NULL);
    printf("Close took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

void test_time_nearest(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000000.0f; i++){
        bool x = roundToNearest(1.5f, f_pi/6);
    }
    gettimeofday(&stop, NULL);
    printf("Nearest took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

void test_time_cos(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000000.0f; i++){
        float input = i / 100000;
        int x = cos_t(input);
    }
    gettimeofday(&stop, NULL);
    printf("Cos took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

void test_time_mathcos(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000000.0f; i++){
        float input = i / 100000;
        int x = cos(input);
    }
    gettimeofday(&stop, NULL);
    printf("Math.h took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

void test_time_tan(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000000.0f; i++){
        float input = i / 1000000;
        int x = tan_t(input);
    }
    gettimeofday(&stop, NULL);
    printf("tan took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

void test_time_mathtan(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000000.0f; i++){
        float input = i / 1000000;
        int x = tan(input);
    }
    gettimeofday(&stop, NULL);
    printf("math.h tan took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

void test_time_arctan(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000.0f; i+=0.001f){
        int x = arctan_t_2(i);
    }
    gettimeofday(&stop, NULL);
    printf("arctan took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

void test_time_matharctan(){
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    for(float i = 0.0f; i < 1000.0f; i+=0.001f){
        int x = atan(i);
    }
    gettimeofday(&stop, NULL);
    printf("math.h arctan took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
}

int main(){
    float res1;
    float res2;
    float res3;
    for(float i = 4.68f; i < 4.74f; i+=0.000001f){
        res1 = (float)sin_t(i) / 1000000;
        res2 = (float)cos_t(i) / 1000000;
        res3 = (float)tan_t(i) / 1000000;
        if(abs(res1) > 1 || abs(res2) > 1){
            printf("sin(%f) = %f, off by: %f\n", i, res1, fabs(res1 - (float)sin(i)));
            printf("cos(%f) = %f, off by: %f\n", i, res2, fabs(res2 - (float)cos(i)));
        }
        if(i < f_pi/2){
            //printf("tan(%f) = %f, off by: %f\n", i, res3, fabs(res3 - (float)tan(i)));
        }
    }
    //test_time_nearest();
    //test_time_close();
    //test_time_closest();
    //test_time_cos();
    //test_time_tan();
    //test_time_mathtan();
    //test_time_mathcos();
    //test_time_arctan();
    //test_time_matharctan();
    return 0;
}

