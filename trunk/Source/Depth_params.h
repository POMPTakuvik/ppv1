// 
//  Depth_params.h
//  
//  Created by Maxime Benoit-Gagne on 2016-12-15.
//  Takuvik - Canada.
//  
//  compiler:
//  $ g++ -v
//  Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
//  Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
//  Target: x86_64-apple-darwin12.6.0
//  Thread model: posix
//  
//  usage:
//  header file only.
//  
//  description:
//   Contains constants for Depth.h and DepthAPI.h.
//  
//  uses: 
//  
//  keywords: C, C++

#ifndef __Depth_params__
#define __Depth_params__

/*
 * Number of geometric depths.
 * The geometric depths are from 0 to 100 by step 1.
 * Units: m.
 */
#define NBDEPTHS 101
/*
 * Number of optical depths.
 * The optical depths are 100%, 90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%, 1%,
 * 0.1%.
 * Units: unitless.
 */
#define NBDEPTHS_OPT 12

#endif /* define(__Depth_params__) */
